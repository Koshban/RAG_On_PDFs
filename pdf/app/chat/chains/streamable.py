from queue import Queue
from threading import Thread
from pdf.app.chat.callbacks.stream import StreamingHandler
from flask import current_app


''' Base Streaming Class that would work for every type of Chains. We can just call it
with overwrite in different classes e.g. below '''
class StreamableChain:
    def stream(self, input: dict):
        queue = Queue() # An individual Queue for every session/object
        handler = StreamingHandler(queue=queue)

        def task(app_context):
            app_context.push() # Gv acces to the flask Object's context within the Task/List e.g. user, DB etc
            self(input, callbacks=[handler])

        '''Use a Thread utilizing concurrency so as to force the LLMChain to execute as it gets the chunks and not wait till the entire message is returned.
        The args=[current_app.app_context() is being passed to the task as an argument to ensure that the Thread has the current Flask Object's Context'''
        Thread(target=task, args=[current_app.app_context()]).start()  

        while True:
            try:
                token = queue.get()
                if token is None:
                    break
                yield token
            except KeyboardInterrupt:
                print("KeyBoard Interrupt Received")
                exit()
