import grpc
from concurrent import futures
import test_pb2_grpc
import test_pb2

class MyService(test_pb2_grpc.MyServiceServicer):
    def StreamData(self, request_iterator, context):
        count = 0
        for request in request_iterator:
            count += 1
            print(f"Received request {count}: {request.data}")
            if count <= 10:
                yield test_pb2.Response(message=f"Received request {count}: {request.data}")
            else:
                break

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_MyServiceServicer_to_server(MyService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
