"""[summary]
"""
from energinetml.core.logger import ConsoleLogger


class TrainingError(Exception):
    pass


class AbstractTrainingContext:
    """
    TODO
    """

    def train_model(self, model, tags, *args, **kwargs):
        """
        :param energinetml.Model model:
        :param typing.Dict[str, typing.Any] tags:
        :rtype: energinetml.TrainedModel
        """
        pass

    def save_output_files(self, model):
        """
        Saves output files from a training run if necessary.

        :param energinetml.Model model:
        """
        pass

    def get_parameters(self, model):
        """
        Returns parameters for a training.

        :param energinetml.Model model:
        :rtype: typing.Dict[str, str]
        """
        return {}

    def get_tags(self, model):
        """
        Returns tags for a training.

        :param energinetml.Model model:
        :rtype: typing.Dict[str, str]
        """
        return {}

    def save_log_file(self, clog: ConsoleLogger) -> None:
        """This function takes the log file generated from clog and
        pushes the log into the azure ml expiremnt tab called output.

        Args:
            clog (ConsoleLogger): This argument is an object of our logger function.

        """
        pass


def requires_parameter(name, typ):
    def requires_parameter_decorator(func):
        def requires_parameter_inner(*args, **kwargs):
            if name not in kwargs:
                raise TrainingError(f'Missing parameter "{name}"')
            try:
                kwargs[name] = typ(kwargs.get(name))
            except ValueError:
                raise TrainingError(
                    (
                        f'Parameter "{name}" could not be cast '
                        f"to type { typ.__name__}: { kwargs.get(name)}"
                    )
                )
            return func(*args, **kwargs)

        return requires_parameter_inner

    return requires_parameter_decorator
