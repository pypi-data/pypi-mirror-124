import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.optimize import minimize

from .tree import BFS, generate_tree
from .cubic_spline import UniformCubicSpline
from collections import deque


class SplineOptimization:

    def __init__(self):
        pass

    @staticmethod
    def initialize_point_cloud(reference_point: np.ndarray,
                               tangent_angle: float,
                               X: np.ndarray) -> np.ndarray:

        # Apply the translation to the point cloud data
        X_aligned = X - reference_point

        # Compute the rotation matrix for the axis
        rotation_matrix: np.ndarray = np.array([[np.cos(tangent_angle), np.sin(tangent_angle)],
                                                [-np.sin(tangent_angle), np.cos(tangent_angle)]])

        # Apply thr rotation to the point cloud
        X_aligned = np.dot(rotation_matrix, X_aligned.transpose()).transpose()

        # Return only the points that
        return X[X_aligned[:, 0] >= 0.2, :]

    @staticmethod
    def order_point_cloud(reference_point: np.ndarray,
                          X: np.ndarray,
                          neighbour_radius: float = 1.0) -> (np.ndarray, np.ndarray):

        # Get the number of points to fit
        num_points, _ = X.shape

        # Compute the KD-Tree with the nearest neighbours
        kd = NearestNeighbors(radius=neighbour_radius, n_neighbors=30)
        kd.fit(X)

        # Compute the adjency matrix to represent the graph of the 2D point cloud
        adj_matrix = kd.radius_neighbors_graph(mode='distance')

        # Compute the closest point to the initial reference
        closest_point_distance, closest_point_index = kd.kneighbors([reference_point], 1, return_distance=True)
        closest_point_distance = closest_point_distance.item()
        closest_point_index = closest_point_index.item()

        adj_matrix = adj_matrix.todense()
        adj_matrix = np.r_[np.zeros((1, num_points)), adj_matrix]
        adj_matrix = np.c_[np.zeros((num_points + 1, 1)), adj_matrix]
        adj_matrix[0, closest_point_index + 1] = closest_point_distance
        adj_matrix[closest_point_index + 1, 0] = closest_point_distance

        # Generate the final adjency list that represent the graph ( with the original reference in it)
        adj_matrix = csr_matrix(adj_matrix)

        # Compute the minimum spanning tree
        T = minimum_spanning_tree(adj_matrix, overwrite=True)

        # Compute the tree starting the reference point (the root node)
        tree = generate_tree(T, num_points + 1)

        # Apply BFS to get the longest path in the tree, starting from the root node
        indexes, distances = BFS(tree[0])

        # Return the final points (including the reference point) ordered to be fitted by the spline
        try:
            # Generate the vector of points to connect
            X = np.vstack([reference_point, X])

            final_points = X[indexes, :]

            # Get the original number of points
            num_points, _ = final_points.shape

            return final_points, distances

        except:
            raise Exception('Could not get list of ordered points to fit')

    @staticmethod
    def prune_points(points: np.ndarray, distances: np.ndarray):

        num_points, _ = points.shape

        distances2 = []
        points2 = []

        curr_distance: float = 0.0
        curr_index: int = 0
        curr_next: int = 1

        points2.append(points[curr_index, :])
        stop: bool = False
        while not stop:

            curr_point = points[curr_index, :]
            next_point = points[curr_next, :]

            curr_distance = np.linalg.norm(curr_point - next_point)
            if curr_distance > 0.3:
                points2.append(next_point)
                distances2.append(curr_distance)
                curr_index = curr_next
                curr_next = curr_index + 1
            else:
                curr_next += 1

            if curr_next >= num_points or curr_index >= num_points - 1:
                stop = True

        return np.array(points2), np.array(distances2)

    @staticmethod
    def generate_initial_tau_vector(distances: np.ndarray, max_tau: float) -> np.ndarray:

        # Get the number of tau_vector to generate
        num_points = distances.size
        num_points += 1

        # Get the total length of the points to fit by straight lines
        length: float = np.sum(distances)

        # Normalize the distances vector so that the sum yield max_tau
        distances: np.ndarray = (distances / length) * max_tau

        # Generate the vector of taus, based on the distance of each point
        tau_vec = np.empty((num_points,))
        tau_vec[0] = 0.0
        for i in range(1, num_points):
            tau_vec[i] = tau_vec[i - 1] + distances[i - 1]

        return tau_vec

    @staticmethod
    def generate_control_points(initial_point: np.ndarray, end_point: np.ndarray, num_control_points: float):

        # Generate a vector of t to use to generate equally spaced control points along a line
        t = np.linspace(start=0.0, stop=1.0, num=num_control_points)

        # Compute the slope of the line
        slope = end_point - initial_point
        slope = np.repeat(slope, num_control_points).reshape((2, num_control_points))

        # Return the control points coordinates in one vector
        return ((slope * t).T + initial_point).reshape((num_control_points * 2,), order='F')

    @staticmethod
    def _cost_function(P: np.ndarray,
                       B: np.ndarray,
                       X: np.ndarray,
                       f: np.ndarray,
                       s: np.ndarray,
                       a1: float = 0.01,
                       a2: float = 0.01) -> float:
        """
        Static method used for computing the cost function value given a spline with a set of control
        points and the points in the 2D space to fit
        :param P - the control points of the curve to fit. A set of point to fit
        :param tau - the path parameter corresponding to the points being fitted
        :param X - the point to fit
        :param curve - the curve object with all the method implementation for the necessary computations
        :param a1 - tuning parameter for first derivative regularization
        :param a2 - tuning parameter for second derivative regularization
        """
        num_points = int(X.size / 2)

        # Compute the norm of the error
        error_vec = np.linalg.norm(np.dot(B, P).reshape((num_points, 2)) - X.reshape((num_points, 2)), axis=1) ** 2

        # Return the cost functional + regularization term
        return np.sum(error_vec) + (a1 * np.dot(P.T, np.dot(f, P))) + (a2 * np.dot(P.T, np.dot(s, P)))

    @staticmethod
    def _control_points_constraint(P: np.ndarray, P0: np.ndarray, num_control_points: int) -> np.ndarray:

        # Compute the expected position of the points on the curve
        Err_x = P0[0:3] - P[0:3]
        Err_y = P0[num_control_points:num_control_points+3] - P[num_control_points:num_control_points+3]
        return np.hstack((Err_x, Err_y))

    @staticmethod
    def _pos_constraint(P: np.ndarray, B_init: np.ndarray, initial_pos: float) -> np.ndarray:

        # Compute the expected position of the points on the curve
        return initial_pos - np.dot(B_init, P)

    def fit_first(self, P0: np.ndarray,
                    tau_vec: np.ndarray,
                    X: np.ndarray,
                    init_pos: np.ndarray,
                    a1: float = 0.1,
                    a2: float = 0.1,
                    max_iterations: int = 100) -> np.ndarray:

        # Get the number of control points to use
        num_control_points, _ = P0.shape
        P0 = P0.reshape((num_control_points * 2,), order='F')

        # Get the number of points to fit
        num_point = int(X.size / 2)

        # Create the initial cubic spline with the specified control points
        curve = UniformCubicSpline(num_control_points=num_control_points, is_closed=False)

        # Compute the Basis Matrix for the spline (the constant part)
        B = curve.getBasis(tau_vec)
        B_init = curve.getBasis(np.asarray([0.0]))

        # Get the Basis Matrix to compute the regularization terms
        r1 = curve.integralFMatrix
        r2 = curve.integralSMatrix

        # Create the function to be optimized (p are the control points to be optimized)
        f = lambda p: self._cost_function(p, B, X, r1, r2, a1, a2)

        # Create the Constraint functions to be applied
        c1 = lambda p: self._pos_constraint(p, B_init, init_pos)

        # Create the constraints list of dictionaries
        cons = ([])

        # Add the position constraint
        con1 = {'type': 'eq', 'fun': c1}
        cons.append(con1)

        # Create a dictionary with solver options
        solver_config = {'maxiter': max_iterations, 'disp': False}

        # Solve the optimization problem
        result = minimize(f, P0, method='SLSQP', constraints=cons, options=solver_config)

        # Return the new control points of the curve
        return result.x.reshape((num_control_points, 2), order='F')

    def fit(self, P0: np.ndarray,
            X: np.ndarray,
            tau_vec: np.ndarray = None,
            a1: float = 0.1,
            a2: float = 0.1,
            max_iterations: int = 100) -> np.ndarray:

        # Get the number of control points to use
        num_control_points, _ = P0.shape
        P0 = P0.reshape((num_control_points*2, ), order='F')

        # Get the number of points to fit
        num_point = int(X.size / 2)

        # Create the initial cubic spline with the specified control points
        curve = UniformCubicSpline(num_control_points=num_control_points, is_closed=False)

        # Compute the Basis Matrix for the spline (the constant part)
        B = curve.getBasis(tau_vec)

        # Get the Basis Matrix to compute the regularization terms
        r1 = curve.integralFMatrix
        r2 = curve.integralSMatrix

        # Create the function to be optimized (p are the control points to be optimized)
        f = lambda p: self._cost_function(p, B, X, r1, r2, a1, a2)

        # Create the Constraint functions to be applied
        c1 = lambda p: self._control_points_constraint(p, P0, num_control_points)

        # Create the constraints list of dictionaries
        cons = ([])

        # Only add the derivatives constrains to the list if we have values for it
        con1 = {'type': 'eq', 'fun': c1}
        cons.append(con1)

        # Create a dictionary with solver options
        solver_config = {'maxiter': max_iterations, 'disp': False}

        # Solve the optimization problem
        result = minimize(f, P0, method='SLSQP', constraints=cons, options=solver_config)

        # Return the new control points of the curve
        return result.x.reshape((num_control_points, 2), order='F')

    def generate_first_spline(self, X: np.ndarray,
                              vehicle_pos: np.ndarray,
                              vehicle_yaw: np.ndarray,
                              num_control_points: int = 10,
                              a1: float = 0.1,
                              a2: float = 0.1,
                              max_dist_neighbours: float = 1.0,
                              max_iterations: int = 100,
                              control_points_adaptive = False,
                              adaptive_density: int = 12) -> (np.ndarray, np.ndarray, float):

        # Triage the point cloud by removing the points of the new path that are behind the vehicle
        X = self.initialize_point_cloud(vehicle_pos, vehicle_yaw, X)

        # Order the point cloud points from the closest to the vehicle to the furthest
        X, distances = self.order_point_cloud(vehicle_pos, X, max_dist_neighbours)
        X, distances = self.prune_points(X, distances)

        # Get the number of new control points for the spline to be fitted
        if control_points_adaptive:
            num_control_points = min(max(int(sum(distances / adaptive_density)), 4), 25)

        # Generate the initial control points for the fit
        P0 = self.generate_control_points(initial_point=X[0, :], end_point=X[-1, :], num_control_points=num_control_points)
        P0 = P0.reshape((num_control_points, 2), order='F')

        # Generate the vector of tau to fit the spline
        tau_vec = self.generate_initial_tau_vector(distances, max_tau=num_control_points - 3)

        # Reshape the Points vector X, in order to be a vector and not a matrix
        num_points, _ = X.shape
        X = X.reshape((num_points * 2,), order='F')

        # Fit the spline to the point cloud
        P_final = self.fit_first(P0, tau_vec, X, vehicle_pos, a1=a1, a2=a2, max_iterations=max_iterations)

        return X.reshape((num_points, 2), order='F'), P0, P_final

    def get_best_gamma(self, path_gamma: float, original_spl: UniformCubicSpline):

        # Get the initial gamma of the next spline section
        start_gamma = int(path_gamma + 1.0)

        # Because my computer is slow simulating the 3D environment, I'm adding a little of slack (should not be needed)
        if start_gamma - path_gamma < 0.3:
            start_gamma += 1

        # Limit the max of the gamma (for safety off course)
        return np.minimum(start_gamma, original_spl.getMaxTau())

    def generate_spline(self, X: np.ndarray,
                        current_gamma: float,
                        control_points: np.ndarray,
                        num_control_points: int = 10,
                        a1: float = 0.1,
                        a2: float = 0.1,
                        max_dist_neighbours: float = 1.0,
                        max_iterations: int = 100,
                        control_points_adaptive=False,
                        adaptive_density: int = 12) -> (np.ndarray, np.ndarray, float):

        # Get the current number of control points (iteration k-1)
        curr_num_control_points, _ = control_points.shape
        spl = UniformCubicSpline(curr_num_control_points, is_closed=False)

        # Get the next gamma for which we will start fitting from
        # For example (if gamma = 0.5) we will start fitting from (gamma = 1) where a transition of control points is located
        #current_gamma = int(current_gamma)
        current_gamma = self.get_best_gamma(current_gamma, spl)
        print(current_gamma)

        # Bounding just to prevent from a nasty bug, where on the limit gamma = 1 and it tries to fit at 2
        max_gamma = spl.getMaxTau()
        current_gamma = np.minimum(current_gamma, max_gamma)

        # Get the current vehicle position and path tangent angle from the current_gamma
        # evaluated with the current control points
        B_curr = spl.getBasis(np.asarray([current_gamma]))
        B_dot_curr = spl.getFirstDerivativeBasis(np.asarray([current_gamma]))

        vehicle_pos = np.dot(B_curr, control_points.reshape((curr_num_control_points * 2,), order='F'))
        first_derivative = np.dot(B_dot_curr, control_points.reshape((curr_num_control_points * 2,), order='F'))
        path_tangent_angle = np.arctan2(first_derivative[1], first_derivative[0])

        # Triage the point cloud by removing the points of the new path that are behind the vehicle
        X = self.initialize_point_cloud(vehicle_pos, path_tangent_angle, X)

        # Check if after the triage we have points to fit (at least 10)
        num_points, _ = X.shape
        if num_points < 10:
           return None, None, None

        # Order the point cloud points from the closest to the vehicle to the furthest
        X, distances = self.order_point_cloud(vehicle_pos, X, max_dist_neighbours)
        X, distances = self.prune_points(X, distances)

        # Get the number of new control points for the spline to be fitted
        if control_points_adaptive:
            num_control_points = min(max(int(sum(distances / adaptive_density)), 4), 25)

        # Generate the initial control points for the fit
        P0 = self.generate_control_points(initial_point=X[0, :], end_point=X[-1, :], num_control_points=num_control_points)

        # Get the index of the last control point that affects the fitting
        index_spline,_ = UniformCubicSpline.internalTauMapFloat(current_gamma)
        control_points_indexes = spl.getControlPointsIndex(int(index_spline))

        # Discard the old control points
        control_points = control_points[0:control_points_indexes[3]+1,:]
        curr_num_control_points, _ = control_points.shape

        # Get the last 3 control points and concatenate with P0
        P0 = np.vstack((control_points[-3:, :], P0.reshape((num_control_points, 2), order='F')))
        num_control_points, _ = P0.shape

        # Generate the vector of tau to fit the spline
        tau_vec = self.generate_initial_tau_vector(distances, max_tau=num_control_points - 3)

        # Reshape the Points vector X, in order to be a vector and not a matrix
        num_points, _ = X.shape
        X = X.reshape((num_points * 2,), order='F')

        # Fit the spline to the point cloud
        P_final = self.fit(P0, X, tau_vec,
                           a1=a1, a2=a2,
                           max_iterations=max_iterations)

        # Concatenate the initial control points, with the final ones
        P_final = np.vstack((control_points[0:curr_num_control_points-3, :], P_final))

        return X.reshape((num_points, 2), order='F'), P0, P_final