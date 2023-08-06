import numpy as np
from scipy import constants
from typing import Tuple, List
from math import degrees, atan
from functools import lru_cache
import tensorflow as tf

pi = constants.pi  # define pi, the ratio of the circumference of a circle to its diameter
g = constants.g    # define the gravitational acceleration on earth, in ms^-2


def terminal_velocity(m: float, A: float, rho: float, c_d: float, g: float = g) -> float:
    """
    Calculate the terminal velocity of an object, given its mass (m), its surface area (A),
    the density of the substance it travels through (rho), the drag coefficient (c_d) and the gravitational acceleration

    :param m: mass of the object in kg
    :param A: surface area of the object in m^2
    :param rho: density of the medium in kgm^-3
    :param c_d: drag coefficient of the object
    :param g: gravitational acceleration of the object in ms^-2
    :return: the terminal velocity in m/s
    """
    return (2*m*g/(rho*A*c_d))**.5


def terminal_velocity_sphere(m: float, d: float, rho: float, g: float = g) -> float:
    """
    Calculate the terminal velocity of a perfect sphere, given its mass (m), its surface diameter (D),
    the density of the substance it travels through (rho), and the gravitational acceleration

    :param m: mass of the sphere in kg
    :param d: diameter of the sphere in m^2
    :param rho: density of the medium in kgm^-3
    :param g: gravitational acceleration of the sphere in ms^-2
    :return: the terminal velocity in m/s
    """
    c_d = .47
    r = d/2
    A = r**2 * pi
    return terminal_velocity(m, A, rho, c_d, g)


def float_input(_prompt: str = '') -> float:
    """Return the input as a float"""
    return float(input(_prompt))


def cartesion_to_polar(x: float, y: float) -> Tuple[float, float]:
    """Turn cartesian coordinates into polar coordinates"""

    radius = (x ** 2 + y ** 2) ** .5

    if x < 0:
        angle = degrees(atan(y / x)) + 180.
    elif x == 0:
        angle = 90. if y >= 0 else 270.
    else:
        angle = degrees(atan(y / x))

    angle = angle
    return radius, angle


def fibonacci_sequence(n) -> List[int]:
    """Generate n+1 terms of the fibonacci sequence"""
    fibo_sequence = [0, 1]
    a, b = fibo_sequence
    for i in range(2, n+1):
        a, b = b, a + b
        fibo_sequence += [b]
    return fibo_sequence


# a showcase of recurrence (in this case of course completely unnecessary) and function decorators
# function values are stored, as in, for 10!, we have to calculate 9!. If we:
# call f(10), and after that call f(9), then f(9) will not be calculated, as it is cached
@lru_cache(maxsize=None)
def factorial(n):
    return n * factorial(n-1) if n else 1


class EstimatePi:

    @staticmethod
    def arctan_method(desired_accuracy: float = None, max_n: int = None) -> Tuple[int, float, float]:
        """
        Use the arctan method to approximate pi, either to a desired accuracy, or an n number of steps

        :returns number of steps taken, distance from the true value of pi, and the found value of pi
        """

        if desired_accuracy is not None:
            stop_condition = lambda accuracy, n, desired_accuracy, max_n: accuracy < desired_accuracy
        elif max_n is not None:
            stop_condition = lambda accuracy, n, desired_accuracy, max_n: n >= max_n
        else:
            return 0, pi, 0.


        s = 0
        n = 0
        while not stop_condition(abs(pi - s), n, desired_accuracy, max_n):
            s += (-1)**n * 4 / (2*n + 1)
            n += 1

        return n, abs(pi - s), s


    @staticmethod
    def monte_carlo_simulation(max_n: int) -> Tuple[float, float]:
        """
        Estimate pi by seeing if randomly distributed points fall within the unit circle

        :param max_n: number of points sampled
        :return: the error, and the estimation of pi according to our method
        """
        coords = np.random.uniform(-1, 1, (2, max_n))
        d = np.sum(coords**2, axis=0)**.5 # using the pythagorean theorem to calculate the distance to the origin

        n_points_in_circle = np.count_nonzero(d <= 1)
        fraction_covered_by_circle = n_points_in_circle / max_n

        pi_estimation = fraction_covered_by_circle * 4

        error = abs(pi_estimation - pi)

        return error, pi_estimation


def functional_std_approximation(f, variables: List[Tuple[float]], size=1000):
    """
    Give a functional approximation of the standard deviation after performing a function on the inputs.
    """
    return np.std(f(*[np.random.normal(m, s, size=size) for m, s in variables]))


def calculus_std_approximation(f, variables: List[Tuple[float]]):
    """
    Give an approximation of the standard deviation after performing a function on the inputs, using calculus.

    Uses the autograd property of tensorflow to calculate the derivatives. 
    """
    tf_variables = [tf.Variable(x[0]) for x in variables]
    # log the variables using GradientTape, so the derivatives can later be easily extracted
    with tf.GradientTape() as tape:
        y = f(*tf_variables)
    derivatives = np.abs(np.array(tape.gradient(y, tf_variables)))

    # add different derivatives using root of the sum of squares
    relative_uncertainties = [(derivative * x[1])**2 for derivative, x in zip(derivatives, variables)]
    uncertainty = np.sum(relative_uncertainties)**.5
    return uncertainty


def unpack_variables(variables: List[Tuple]):
    """
    Unpack variables so they can be used for std_approximation. (Think of reshaping, turning into numpy arrays, etc).
    """
    shapes = [np.array(variable[0]).shape for variable in variables] + [(1,)]
    cast_shape = max(shapes, key=len)
    return [(cast_to(variable[0], cast_shape), cast_to(variable[1], cast_shape)) 
            for variable in variables], cast_shape


def eval(f, variables):
    return f(*[variable[0] for variable in variables])


def cast_to(variable: List[Tuple], shape: Tuple[int]):
    """
    Return the variables as numpy arrays to be easily passed into the calculus and functional methods.
    """
    v_shape = np.array(variable).shape
    cast_shape = []
    orig_shape = []
    i = 0
    for dim in shape:
        if i < len(v_shape) and dim == v_shape[i]:
            cast_shape += [1]
            orig_shape += [v_shape[i]]
            i += 1
            continue
        cast_shape += [dim]
        orig_shape += [1]
    return np.array(variable).reshape(orig_shape)*np.ones(cast_shape)


def std_approximation(f, variables: List[Tuple[float, float]], approx_type: str = 'functional', evaluate: bool = False, *args, **kwargs):
    """
    :input f: any function that takes the given variables as input
    :input variables: a list of variables in the form of (value, std). Variables should be given in the same order,
                      as they are to be passed to the function in question. Numpy arrays are also accepted.
    :input approx_type: either 'functional' or 'calculus', to specify which type of approximation to use.
                        - functional: accurate
                        - calculus: fast and stable
    :input evaluate: determine whether the value of the function using the starting values as input should also be returned.
    
    :returns: the standard deviation of the function given variables and their respective standard deviations
    """
    unpacked, cast_shape = unpack_variables(variables)

    if approx_type == 'functional':
        approx_f = functional_std_approximation
    elif approx_type == 'calculus':
        approx_f = calculus_std_approximation
    else:
        print("This type of approximation is not supported")

    std = []
    evaluations = []
    for i in range(cast_shape[0]):
        var_slice = [(var[0][i], var[1][i]) for var in unpacked]
        std += [approx_f(f, var_slice, *args, **kwargs)]
        evaluations += [eval(f, var_slice)]
    std = np.array(std)
    if evaluate:
        return np.squeeze(std), evaluations[0] if len(evaluations) <= 1 else np.array(evaluations)
    return np.squeeze(std)






