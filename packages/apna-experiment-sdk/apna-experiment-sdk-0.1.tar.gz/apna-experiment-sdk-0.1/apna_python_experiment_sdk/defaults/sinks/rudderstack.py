from typing import List
from apna_python_experiment_sdk.base import Configuration, SinkSerializer, Sink
import rudder_analytics
from datetime import date, datetime
import logging


class RudderstackConf(Configuration):
    """Configuration for rudderstack.
    Needs the following variables:
    TODO: (Mention enviornment variables.)    
    """
    # TODO: Remove these and add enviornment variables to the code.
    conf = dict(
        write_key="1zR8uE8OvtTKGbDn9mvSNDUOUSF",
        data_plane_url="http://34.93.20.228",
        # TODO: Remove these conf as these are debug conf:
        # flush_interval=200000
        flush_interval=1,
        flush_at=2000
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print('Rudderstack conf: ', self.conf)


class RudderstackSerializer(SinkSerializer):
    def serialize(self, element):
        return {
            "user_id": element['context']['userId'],
            "type": "track",
            "event_name": "$experiment_started",
            "properties": {
                'Experiment name': element['feature'],
                'Variant name': element['variant']['name']
            },
            "timestamp": datetime.now(),
            # "integrations": {
            #     "All"
            # }
        }


class RudderstackSink(Sink):
    client = None

    def __init__(self, configuration: Configuration = RudderstackConf(), serializer: SinkSerializer = RudderstackSerializer()):
        super().__init__(configuration, serializer)

        if self.client is None:
            # Initialize conf and serializer:
            self.configuration = configuration
            self.serializer = serializer

            conf = self.configuration.get_conf()

            # Initialize rudder client:
            rudder_analytics.default_client = rudder_analytics.Client(
                write_key=conf['write_key'],
                host=conf['data_plane_url'],
                flush_interval=conf['flush_interval'],
            )

            self.client = rudder_analytics
            self.client.write_key = conf['write_key']
            self.client.data_plane_url = conf['data_plane_url']

            logging.info('Ruddersink initialzed!')
        else:
            logging.warning(
                f'Ruddersink is already initialized. To recreate instance, you need to destroy exisiting one first.')

    def push(self, element: dict) -> bool:
        """This method calls the 'track' method of the rudderstack clients.
        It requires 'user_id', 'event' and 'properties'.

        Args:
            element (dict): The variant and user_id fetched from experiment_client.

        Returns:
            bool: Returns true if success.
        """
        serialized_data = self.serializer.serialize(element)

        try:
            self.client.track(
                user_id=serialized_data['user_id'],
                event=serialized_data['event_name'],
                properties=serialized_data['properties'],
                timestamp=serialized_data['timestamp']
            )
            logging.debug(f'Element: {serialized_data} tracked.')
        except Exception as e:
            logging.error(f'Exception occured in RudderstackSink `push`: {e}')
            raise e

        return True

    def bulk_push(self, serialized_elements: List[dict]) -> bool:
        raise NotImplementedError(
            f'This function is not implemented and not required in RudderstackSink.')

    def trigger(self):
        raise NotImplementedError(
            f'This function is not implemented and not required in RudderstackSink.')

    def trigger_condition(self) -> bool:
        raise NotImplementedError(
            f'This function is not implemented and not required in RudderstackSink.')
