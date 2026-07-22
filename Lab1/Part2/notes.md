# Useful Notes

## Commands

### Generate Protobuf
```
python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. messages.proto
```