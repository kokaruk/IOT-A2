# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""
from __future__ import print_function

import grpc

from app import helloworld_pb2_grpc, helloworld_pb2


def notify(host, message):
    """
    Sends grpc message to server.
    :param ip of host:
    :param String message:
    :return: response from host
    """
    with grpc.insecure_channel('{}:50051'.format(host)) as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name=message))
        print("Greeter client received: " + response.message)
        return response
