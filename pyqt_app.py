import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QSpinBox
import grpc
import search_pb2 as search_pb2
import search_pb2_grpc as search_pb2_grpc

class QueryApp(QWidget):
    def __init__(self):
        super().__init__()

        self.grpc_channel = grpc.insecure_channel('localhost:50051')
        self.stub = search_pb2_grpc.SearchServiceStub(self.grpc_channel)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('gRPC Query App')

        layout = QVBoxLayout()

        self.query_label = QLabel('Query:', self)
        layout.addWidget(self.query_label)

        self.query_input = QLineEdit(self)
        self.query_input.textChanged.connect(self.sent_request)  # Schedule request on text change
        layout.addWidget(self.query_input)

        self.page_label = QLabel('Page:', self)
        layout.addWidget(self.page_label)

        self.page_input = QSpinBox(self)
        self.page_input.setValue(1)  # Default value
        self.page_input.setMinimum(1)  # Limit must be at least 1
        self.page_input.valueChanged.connect(self.sent_request)
        layout.addWidget(self.page_input)

        self.limit_label = QLabel('Limit:', self)
        layout.addWidget(self.limit_label)

        self.limit_input = QSpinBox(self)
        self.limit_input.setValue(10)
        self.limit_input.setMinimum(1)  # Limit must be at least 1
        self.limit_input.setSingleStep(10)
        self.limit_input.valueChanged.connect(self.sent_request)
        layout.addWidget(self.limit_input)

        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)  # Make result text read-only
        layout.addWidget(self.result_text)

        self.setLayout(layout)

    def sent_request(self):
        query = self.query_input.text()
        page = self.page_input.text()
        limit = self.limit_input.text()

        # Validate input
        if not query:
            self.update_results("Please enter a query.")
            return
        if not page.isdigit() or not limit.isdigit():
            self.update_results("Page and Limit must be numeric.")
            return

        # Create the request
        request = search_pb2.QueryRequest(query=query, page=int(page)-1, limit=int(limit))

        print(f"Sending request: {request}")

        try:
            # Send the request and get the response
            response_iterator = self.stub.StreamQuery(self.generate_requests(request))
            self.process_responses(response_iterator)
        except grpc.RpcError as e:
            error_message = f"gRPC error: {e.details()}"
            self.update_results(error_message)
            print(error_message)

    def generate_requests(self, initial_request):
        yield initial_request
        # Continue yielding requests if needed (e.g., based on user input or another logic)
        while False:  # This can be updated to yield more requests if needed
            pass

    def process_responses(self, response_iterator):
        results = []
        for response in response_iterator:
            results.append(f"Total hits: {response.total_hits}\n")
            for item in response.items:
                result = f"name: {item.name}, location: {item.location}"
                results.append(result)
        self.update_results("\n".join(results))

    def update_results(self, result):
        self.result_text.setText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QueryApp()
    ex.show()
    sys.exit(app.exec())
