'''Utility functions for producer & consumer files.'''

def delivery_report(err, msg):
    if err:
        print("Failed to deliver message: {0}: {1}"
              .format(msg.value(), err.str()))
    else:
        print(f"msg produced. \n"
                    f"Topic: {msg.topic()} \n" +
                    f"Partition: {msg.partition()} \n" +
                    f"Offset: {msg.offset()} \n" +
                    f"Timestamp: {msg.timestamp()} \n")



                    
    
