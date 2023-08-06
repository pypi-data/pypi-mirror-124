from numpy import ndarray, array, zeros, ones, asarray, dot, floor, all, clip, stack, power


class UniformCubicSpline:

    def __init__(self, num_control_points: int, is_closed: bool = False):

        # The number of control points to use to represent the curve
        self._num_control_points: int = num_control_points

        # Curve parameters
        self._degree: int = 3  # CUBIC B-SPLINE

        # Save whether the shape is going to be closed or open
        self._is_closed = is_closed

        # Compute the number of segments of the curve
        self._num_segments = (self._num_control_points if self._is_closed else self._num_control_points - self._degree)

        # Validate if the number of segments is greater than zero
        if self._num_segments <= 0:
            raise ValueError('Number of curve segments <= 0 (= {})'.format(self._num_segments))

        # Compute the max value for the tau in the curve
        self._max_tau = self._num_segments  # UNIFORM CURVE

        # Constant matrix used to generate the Cubic B-Spline
        self._basis_matrix: ndarray = array([[-1, 3, -3, 1],
                                             [3, -6, 3, 0],
                                             [-3, 0, 3, 0],
                                             [1, 4, 1, 0]], dtype=float)

        # Constant matrix used to generate the integral of the norm of the first derivative
        self._cm: ndarray = 1 / 6.0 * array([[-1, 3, -3, 1],
                                             [3, -6, 3, 0],
                                             [-3, 0, 3, 0]], dtype=float)

        self._tm: ndarray = array([[3, 0, 0],
                                   [0, 2, 0],
                                   [0, 0, 1]], dtype=float)

        self._t_integral: ndarray = array([[1 / 5, 1 / 4, 1 / 3],
                                           [1 / 4, 1 / 3, 1 / 2],
                                           [1 / 3, 1 / 2, 1 / 1]], dtype=float)

        self._t_integral_const: ndarray = dot(self._cm.transpose(),
                                              dot(self._tm.transpose(),
                                                  dot(self._t_integral,
                                                      dot(self._tm, self._cm))))

        # Constant matrix used to generate the integral of the norm of the second derivative
        self._cm2: ndarray = 1 / 6.0 * array([[-1, 3, -3, 1],
                                              [3, -6, 3, 0]])

        self._tm2: ndarray = array([[6, 0],
                                    [0, 2]])

        self._t_integral2: ndarray = array([[1 / 3, 1 / 2],
                                            [1 / 2, 1 / 1]])

        self._t_integral2_const: ndarray = dot(self._cm2.transpose(),
                                               dot(self._tm2.transpose(),
                                                   dot(self._t_integral2,
                                                       dot(self._tm2, self._cm2))))

        # Compute the actual integral matrices
        self._integralFMatrix = self._computeIntegralMatrix(order=1)
        self._integralSMatrix = self._computeIntegralMatrix(order=2)

    @staticmethod
    def internalTauMapFloat(tau: float) -> ():
        i = floor(tau)
        if i == tau:
            i = i-1
        t = tau - i
        assert (0.0 <= t) & (t <= 1.0)
        return i, t

    @staticmethod
    def internalTauMap(tau) -> (ndarray, ndarray):
        """
        Method that maps a curve parameter to a a specific spline
        :param tau: The curve parameter
        :return: A tuple with the segment index that is belongs to and the corresponding curve parameter inside the spline
        """

        # Compute the segment index corresponding to this tau
        i = floor(tau).astype(int)

        # Apply a correction if we are on the limit of the end of the spline
        i[i == tau] = i[i == tau] - 1

        # Compute the curve parameter inside that segment
        t = tau - i

        # Make sure that the value of the curve parameter is bounded between 0 and 1
        assert all((0.0 <= t) & (t <= 1.0))

        return i, t

    def clipTau(self, tau) -> float:
        """
        Clips the values of the curve parameter to the domain of the contour
        :param tau: The curve parameter
        :return: The clipped curve parameter
        """
        return (asarray(tau) % self._num_segments) if self._is_closed else clip(tau, 0.0, self._max_tau)

    def getControlPointsIndex(self, i: int) -> ndarray:
        """
        Method that given a segment index, returns a list with the index of the control points
        :param i: The index of the spline that we want the control points for
        :return: The index of the controls points (in the vector of control points)
        """
        return array([i % self._num_control_points for i in range(i, i + self._degree + 1)])

    def getMaxTau(self) -> float:
        """
        Method that returns the maximum value of the path parameter
        :return: A float with the maximum value of the path parameter
        """
        return self._max_tau

    @property
    def integralFMatrix(self) -> ndarray:
        """
        :return: An ndarray with [2N, 2N] matrix corresponding to the integral of the norm of the first
        derivative of the path with respect to tau
        N = the number of control points
        To obtain the integral value, just multiply [control_points * integralMatrix * control_points']
        """
        return self._integralFMatrix

    @property
    def integralSMatrix(self) -> ndarray:
        """
        :return: An ndarray with [2N, 2N] matrix corresponding to the integral of the norm of the second
        derivative of the path with respect to tau
        N = the number of control points
        To obtain the integral value, just multiply [control_points * integralMatrix * control_points']
        """
        return self._integralSMatrix

    def getBasis(self, tau: ndarray) -> ndarray:

        # Make sure that the curve parameter is interpreted as an array (to allow for vectorial access)
        tau = asarray([tau]).reshape((tau.size,))

        # Compute the index of the spline corresponding to the curve parameter and the normalized parameter for that spline
        index_spline, t_spline = UniformCubicSpline.internalTauMap(tau)

        # Compute the tau vector
        tau_vec: ndarray = stack([asarray(power(t_spline, 3)),
                                  asarray(power(t_spline, 2)),
                                  asarray(t_spline),
                                  ones(tau.size)], axis=0).transpose()

        # Compute the Basis matrix
        B = zeros((2 * tau.size, 2 * self._num_control_points), dtype=float)

        # For each value of tau
        B_aux = 1.0 / 6.0 * dot(tau_vec, self._basis_matrix)

        for i in range(tau.size):
            # Get the indexes of the control points to be used
            control_points_indexes: ndarray = self.getControlPointsIndex(index_spline[i])

            # Save the values in the right place in the Basis matrix
            B[i, control_points_indexes] = B_aux[i, :]
            B[i + tau.size, control_points_indexes + self._num_control_points] = B_aux[i, :]

        return B

    def getFirstDerivativeBasis(self, tau: ndarray) -> ndarray:

        # Make sure that the curve parameter is interpreted as an array (to allow for vectorial access)
        tau = asarray([tau]).reshape((tau.size,))

        # Compute the index of the spline corresponding to the curve parameter and the normalized parameter for that spline
        index_spline, t_spline = UniformCubicSpline.internalTauMap(tau)

        # Compute the tau vector
        tau_vec: ndarray = stack([3 * (t_spline ** 2),
                                  2 * t_spline,
                                  ones(tau.size),
                                  zeros(tau.size)], axis=0).transpose()

        # Save the values of the curve for each tau value
        B_dot = zeros((2 * tau.size, 2 * self._num_control_points), dtype=float)

        # For each value of tau
        B_dot_aux = 1.0 / 6.0 * dot(tau_vec, self._basis_matrix)

        for i in range(tau.size):
            # Get the indexes of the control points to be used
            control_points_indexes: ndarray = self.getControlPointsIndex(index_spline[i])

            # Save the values in the right place in the basis matrix
            B_dot[i, control_points_indexes] = B_dot_aux[i, :]
            B_dot[i + tau.size, control_points_indexes + self._num_control_points] = B_dot_aux[i, :]

        return B_dot

    def getSecondDerivativeBasis(self, tau: ndarray) -> ndarray:

        # Make sure that the curve parameter is interpreted as an array (to allow for vectorial access)
        tau = asarray([tau]).reshape((tau.size,))

        # Compute the index of the spline corresponding to the curve parameter and the normalized parameter for that spline
        index_spline, t_spline = UniformCubicSpline.internalTauMap(tau)

        # Compute the tau vector
        tau_vec: ndarray = stack([6 * asarray(t_spline),
                                  2 * ones(tau.size),
                                  zeros(tau.size),
                                  zeros(tau.size)], axis=0).transpose()

        # Save the values of the curve for each tau value
        B_ddot = zeros((2 * tau.size, 2 * self._num_control_points), dtype=float)

        # For each value of tau
        B_ddot_aux = 1.0 / 6.0 * dot(tau_vec, self._basis_matrix)

        for i in range(tau.size):
            # Get the indexes of the control points to be used
            control_points_indexes: ndarray = self.getControlPointsIndex(index_spline[i])

            # Save the values in the right place in the basis matrix
            B_ddot[i, control_points_indexes] = B_ddot_aux[i, :]
            B_ddot[i + tau.size, control_points_indexes + self._num_control_points] = B_ddot_aux[i, :]

        return B_ddot

    @staticmethod
    def evaluate(basis: ndarray, control_points: ndarray) -> ndarray:
        """
        Evaluate the cubic B-spline at a given set of points
        :param basis:
        :param control_points:
        :return:
        """
        return dot(basis, control_points)

    def _computeIntegralMatrix(self, order: int = 1):

        # Dictionary to save which matrix to access depending on the order
        order_matrix = {1: self._t_integral_const, 2: self._t_integral2_const}

        # Choose the matrix to use depending on the order of the derivative
        integral_aux_matrix = order_matrix[order]

        # Create a matrix to store the values needed for the optimization problem (for the first integral regularization term)
        integral_matrix: ndarray = zeros((2 * self._num_control_points, 2 * self._num_control_points))

        # For each section of the spline
        for spline_index in range(self._num_segments):

            # Get the corresponding control points
            control_points_index: ndarray = self.getControlPointsIndex(spline_index)

            for i in range(len(control_points_index)):
                for j in range(len(control_points_index)):
                    integral_matrix[control_points_index[i], control_points_index[j]] += integral_aux_matrix[i, j]
                    integral_matrix[self._num_control_points + control_points_index[i], self._num_control_points +
                                    control_points_index[j]] += integral_aux_matrix[i, j]

        return integral_matrix
