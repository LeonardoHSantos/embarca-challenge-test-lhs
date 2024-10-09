# Embarca Challenge Test - DevOps Project

Este projeto envolve a criação de uma arquitetura DevOps utilizando tecnologias como **Python**, **Docker**, **AWS Lambda**, **ECR**, **S3** e **RDS (MySQL)**.

## Arquivos Principais de Configuração:

### Docker:
- **Dockerfile**: Localizado em `docker-lambda-image-custom/Dockerfile`, contém as instruções para a criação da imagem Docker usada na função Lambda.
  - O arquivo está detalhadamente comentado para facilitar o entendimento de cada passo.

### GitHub Actions:
- **Pipeline CI/CD**: Arquivo `.github/workflows/ecr-deploy.yml` contém o pipeline que faz o build e deploy da imagem Docker para o Amazon ECR.
  - Comentários detalhados explicam cada parte da configuração.

## Pré-requisitos

1. **Conta AWS**: É necessário ter acesso a uma conta AWS para utilizar serviços como ECR, Lambda e RDS.
2. **Chaves de Acesso AWS**: Você precisará das chaves de acesso (`AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`) que podem ser geradas no serviço IAM.
3. **Docker**: Instale Docker em sua máquina para testar e construir imagens localmente.
4. **GitHub Actions**: Configurado no repositório para CI/CD.

## Configuração das Chaves AWS no GitHub Actions

1. No repositório GitHub, vá em **Settings**.
2. Na seção **Security**, clique em **Secrets and variables** e selecione **Actions**.
3. Clique em **New repository secret** e adicione:
   - `AWS_ACCESS_KEY_ID`: A chave de acesso da sua conta AWS.
   - `AWS_SECRET_ACCESS_KEY`: A chave secreta da sua conta AWS.

Essas chaves podem ser obtidas no console da AWS em **IAM > Credenciais de segurança > Chaves de acesso**.

## Etapa 1 - Criar Repositório AWS ECR (Container)

1. No console AWS, busque por **ECR**.
2. Crie um novo repositório, fornecendo um nome claro e conciso.
3. Selecione a opção **Mutable** para permitir a atualização das imagens.
4. Escolha a criptografia **AES-256**.
5. Clique em **Criar**.

Após um **push** para a branch `main`, o pipeline do GitHub Actions será acionado para fazer o build e enviar a imagem Docker para o ECR.

### Exemplo visual da criação de um repositório ECR:

![Criar repositório AWS ECR](img/image_criacao_container_aws_ERR.png)

## Etapa 2 - Criar Função AWS Lambda

1. No console AWS, busque por **Lambda**.
2. Clique em **Criar função**.
3. Escolha a opção **Imagem de container**.
4. Nomeie a função de maneira descritiva.
5. Insira a **URI** da imagem Docker do ECR.
6. Escolha a arquitetura **x86_64**.
7. Clique em **Criar função**.

### Exemplo visual da criação da função Lambda:

![Criar função Lambda](img/image_criacao_funcao_lambda.png)

## Etapa 3 - Configurar URL da Função Lambda

1. Dentro da função Lambda, vá em **Configuração** e selecione **URL da função**.
2. Clique em **Criar** ou **Editar** para adicionar uma URL.
3. Configure o CORS conforme necessário (neste projeto foi usado `*` para aceitar todas as origens).
4. Clique em **Criar URL**.

### Exemplo visual da configuração da URL da função Lambda:

![Configurar URL da Função Lambda](img/image_criacao_URL_FUNCAO_LAMBDA.png)

## Etapa 4 - Executar o Pipeline de Build e Deploy no GitHub Actions

1. O pipeline é acionado automaticamente após um **push** na branch `main`.
2. Certifique-se de que os arquivos no diretório `docker-lambda-image-custom` foram modificados para acionar o build.

### Exemplo de execução bem-sucedida no GitHub Actions:

![Ação no GitHub](img/image_action_exec_github.png)

## Etapa 5 - Atualizar a Imagem no AWS Lambda

1. Após a conclusão do build, vá para a função Lambda.
2. Atualize a função com a nova imagem Docker gerada.
3. **Importante**: Certifique-se de que a URI da imagem no ECR está correta ou simplesmente clique em **Salvar** para aplicar a nova imagem.

### Exemplo visual de atualização da função Lambda com a nova imagem:

![Atualizar função Lambda](img/image_build_action.png)
