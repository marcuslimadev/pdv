# PDV System - Interface Web

UI web complementar para o sistema PDV desktop.

## 🚀 Início Rápido

### Instalação das Dependências Web

```bash
pip install flask flask-cors
```

Ou instale todas as dependências:

```bash
pip install -r requirements.txt
```

### Executar Interface Web

```bash
python web_app.py
```

A aplicação estará disponível em: **http://localhost:5000**

### Executar Interface Desktop (tradicional)

```bash
python main.py
```

## 📋 Funcionalidades Web

### Dashboard
- Visualização de estatísticas em tempo real
- Total de vendas do dia
- Produtos com estoque baixo
- Total de produtos cadastrados

### Gestão de Produtos
- Listagem completa de produtos
- Filtros por categoria e status
- Busca por nome ou código
- Visualização detalhada

### Consulta de Vendas
- Filtro por período
- Resumo de vendas
- Totalizadores

### Configurações (Admin)
- Configuração de divisão PIX
- Simulador de valores
- Percentuais cliente/plataforma

## 🔐 Autenticação

Use as mesmas credenciais do sistema desktop:

**Administrador:**
- Usuário: `admin`
- Senha: `admin123`

**Operador:**
- Usuário: `operador`
- Senha: `operador123`

## 🌐 API REST

### Endpoints Disponíveis

#### Autenticação
- `POST /login` - Autenticação de usuário
- `GET /logout` - Logout

#### Produtos
- `GET /api/produtos` - Lista todos os produtos
- `GET /api/produtos/<id>` - Obtém produto específico
- `POST /api/produtos` - Cria novo produto (admin)
- `PUT /api/produtos/<id>` - Atualiza produto (admin)

#### Categorias
- `GET /api/categorias` - Lista todas as categorias

#### Vendas
- `GET /api/vendas/resumo` - Resumo de vendas por período

#### Configurações (Admin)
- `GET /api/configuracoes/pix-split` - Obtém config PIX
- `PUT /api/configuracoes/pix-split` - Atualiza config PIX

#### Estatísticas
- `GET /api/estatisticas/dashboard` - Dados do dashboard

### Exemplo de Requisição API

```python
import requests

# Login
response = requests.post('http://localhost:5000/login', json={
    'username': 'admin',
    'senha': 'admin123'
})

# Lista produtos
response = requests.get('http://localhost:5000/api/produtos')
produtos = response.json()
```

## 🎨 Interface

- **Bootstrap 5** para UI responsiva
- **Bootstrap Icons** para ícones
- **jQuery** para manipulação DOM
- Design moderno e intuitivo

## 📱 Responsivo

A interface web é totalmente responsiva e funciona em:
- Desktop
- Tablets
- Smartphones

## ⚙️ Configuração

O servidor web roda por padrão em:
- **Host:** 0.0.0.0 (acessível na rede local)
- **Porta:** 5000
- **Debug:** Ativado (desative em produção)

## 🔄 Integração

Ambos sistemas (desktop e web) compartilham:
- Mesmo banco de dados
- Mesmos DAOs e Services
- Mesma autenticação
- Mesmas configurações

## 📊 Vantagens da Interface Web

1. **Acesso Remoto** - Gerencie de qualquer lugar
2. **Multiplataforma** - Funciona em qualquer SO
3. **Sem Instalação** - Basta um navegador
4. **API REST** - Integrações facilitadas
5. **Dashboard** - Visualização em tempo real

## 🛡️ Segurança

- Autenticação por sessão
- Decorators para proteção de rotas
- Separação de permissões (admin/operador)
- CORS configurado

## 🔧 Desenvolvimento

Para desenvolvimento ativo:

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

Para produção, use um servidor WSGI como **Gunicorn**:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

## 📝 Notas

- A interface web é **complementar** ao sistema desktop
- O desktop continua sendo a interface principal para operação de caixa
- Use a web para gestão, consultas e configurações remotas
