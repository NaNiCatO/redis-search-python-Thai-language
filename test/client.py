import grpc
import test_pb2
import test_pb2_grpc

def generate_requests():
    while True:
        data = input("Enter data (or 'quit' to exit): ")
        if data.lower() == 'quit':
            break
        yield test_pb2.Request(data=data)

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = test_pb2_grpc.MyServiceStub(channel)
        try:
            response_iterator = stub.StreamData(generate_requests())
            for response in response_iterator:
                print("Response:", response.message)
        except grpc.RpcError as e:
            print(f"RPC error: {e}")

if __name__ == '__main__':
    run()
