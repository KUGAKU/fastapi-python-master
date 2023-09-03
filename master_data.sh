#!/bin/bash

# This script is used to generate the master data for the project
python3 -c "
print('start to create master data')
from models.message_type import MessageType, MessageTypeEnum
from settings import Session
session = Session()

message_type = MessageType()
message_type.message_type_id = MessageTypeEnum.HUMAN.value
message_type.message_type_name = 'Human'
session.add(message_type)

message_type = MessageType()
message_type.message_type_id = MessageTypeEnum.ARTIFICIAL_INTELLIGENCE.value
message_type.message_type_name = 'Artificial Intelligence'
session.add(message_type)

session.commit()

print('success!')
"
