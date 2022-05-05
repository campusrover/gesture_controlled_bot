# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import boto3
import ask_sdk_core.utils as ask_utils
import Credentials
from datetime import datetime

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

my_credentials = Credentials.Credentials()

sqs = boto3.client('sqs', region_name = 'us-east-2',
                    aws_access_key_id=my_credentials.AWS_ACCESS_KEY_ID, 
                    aws_secret_access_key=my_credentials.SECRET_ACCESS_KEY)

queue = sqs.get_queue_url(QueueName=my_credentials.vcq_name,
                            QueueOwnerAWSAccountId=my_credentials.OWNER_ID)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say move mini scout forward or help. you have ten seconds between each command to modify movement or the robot will stop"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class MoveIntentHandler(AbstractRequestHandler):
    """Handler for Move Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("Move")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "moving"
        intent_name = ask_utils.get_intent_name(handler_input)
        current_time = datetime.now()
        sqs_message = {"Motion Input": "Alexa", "Intent": intent_name, "Current Time":current_time.strftime("%H:%M:%S")}
        sqs.send_message(QueueUrl= queue['QueueUrl'],
                                    MessageBody= str(sqs_message), 
                                    MessageGroupId='testing_voice_data')
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("")
                .response
        )

class MoveForwardIntentHandler(AbstractRequestHandler):
    """Handler for MoveForward Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("MoveForward")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "moving mini scout forward"
        intent_name = ask_utils.get_intent_name(handler_input)
        current_time = datetime.now()
        sqs_message = {"Motion Input": "Alexa", "Intent": intent_name, "Current Time":current_time.strftime("%H:%M:%S")}
        sqs.send_message(QueueUrl= queue['QueueUrl'],
                                    MessageBody= str(sqs_message), 
                                    MessageGroupId='testing_voice_data')
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("")
                .response
        )

class RotateLeftIntentHandler(AbstractRequestHandler):
    """Handler for RotateLeft Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RotateLeft")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "turning mini scout left"
        intent_name = ask_utils.get_intent_name(handler_input)
        current_time = datetime.now()
        sqs_message = {"Motion Input": "Alexa", "Intent": intent_name, "Current Time":current_time.strftime("%H:%M:%S")}
        sqs.send_message(QueueUrl= queue['QueueUrl'],
                                    MessageBody= str(sqs_message), 
                                    MessageGroupId='testing_voice_data')
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("")
                .response
        )

class RotateRightIntentHandler(AbstractRequestHandler):
    """Handler for RotateRight Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RotateRight")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "turning mini scout right"
        intent_name = ask_utils.get_intent_name(handler_input)
        current_time = datetime.now()
        sqs_message = {"Motion Input": "Alexa", "Intent": intent_name, "Current Time":current_time.strftime("%H:%M:%S")}
        sqs.send_message(QueueUrl= queue['QueueUrl'],
                                    MessageBody= str(sqs_message), 
                                    MessageGroupId='testing_voice_data')
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("")
                .response
        )

class MoveBackwardIntentHandler(AbstractRequestHandler):
    """Handler for MoveBackward Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("MoveBackward")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "moving mini scout backwards"
        intent_name = ask_utils.get_intent_name(handler_input)
        current_time = datetime.now()
        sqs_message = {"Motion Input": "Alexa", "Intent": intent_name, "Current Time":current_time.strftime("%H:%M:%S")}
        sqs.send_message(QueueUrl= queue['QueueUrl'],
                                    MessageBody= str(sqs_message), 
                                    MessageGroupId='testing_voice_data')
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("")
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "here are some things you can say: move forward or move backwards"
        # intent_name = ask_utils.get_intent_name(handler_input)
        # current_time = datetime.now()
        # sqs_message = {"Motion Input": "Alexa", "Intent": intent_name, "Current Time":current_time.strftime("%H:%M:%S")}
        # sqs.send_message(QueueUrl= queue['QueueUrl'],
        #                             MessageBody= str(sqs_message), 
        #                             MessageGroupId='testing_voice_data')
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "stopping"
        intent_name = ask_utils.get_intent_name(handler_input)
        current_time = datetime.now()
        sqs_message = {"Motion Input": "Alexa", "Intent": intent_name, "Current Time":current_time.strftime("%H:%M:%S")}
        sqs.send_message(QueueUrl= queue['QueueUrl'],
                                    MessageBody= str(sqs_message), 
                                    MessageGroupId='testing_voice_data')
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class StopIntentHandler(AbstractRequestHandler):
    """Single handler for Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "stopping"
        intent_name = ask_utils.get_intent_name(handler_input)
        current_time = datetime.now()
        sqs_message = {"Motion Input": "Alexa", "Intent": intent_name, "Current Time":current_time.strftime("%H:%M:%S")}
        sqs.send_message(QueueUrl= queue['QueueUrl'],
                                    MessageBody= str(sqs_message), 
                                    MessageGroupId='testing_voice_data')
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "i'm not sure what movement you meant."
        reprompt = "I didn't get that. What would you like me to do?"
        
        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."
        current_time = datetime.now()
        sqs_message = {"Motion Input": "Alexa", "Intent": intent_name, "Current Time":current_time.strftime("%H:%M:%S")}
        sqs.send_message(QueueUrl= queue['QueueUrl'],
                                    MessageBody= str(sqs_message), 
                                    MessageGroupId='testing_voice_data')

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble moving the way you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(MoveIntentHandler())
sb.add_request_handler(MoveForwardIntentHandler())
sb.add_request_handler(MoveBackwardIntentHandler())
sb.add_request_handler(RotateRightIntentHandler())
sb.add_request_handler(RotateLeftIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelIntentHandler())
sb.add_request_handler(StopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()