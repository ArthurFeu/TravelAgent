# Usar AWS base image para python 3.12
FROM public.ecr.aws/lambda/python:3.12

# instalar build-essential compiler and tools
RUN microdnf update -y && microdnf install -y gcc-c++ make

#copiar dependencias

COPY requirements.txt ${LAMBDA_TASK_ROOT}

# instalar dependencias

RUN pip install -r requirements.txt

# copiar o código fonte

COPY travelAgent.py ${LAMBDA_TASK_ROOT}

# definir permissões

RUN chmod +x travelAgent.py

# definir handler

CMD ["travelAgent.lambda_handler"]