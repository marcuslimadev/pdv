"""
Aplicação web Flask para gestão remota do PDV.
Complementa a interface desktop, permitindo acesso via navegador.
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for, make_response
from flask_cors import CORS
from functools import wraps
from datetime import datetime, timedelta
from decimal import Decimal
import os
import secrets

from src.services.auth_service import auth_service
from src.dao.produto_dao import ProdutoDAO
from src.dao.categoria_dao import CategoriaDAO
from src.dao.venda_dao import VendaDAO
from src.dao.usuario_dao import UsuarioDAO
from src.services.config_service import config_service
from src.utils.formatters import Formatters
from src.utils.logger import Logger

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Chave secreta segura
CORS(app)

# Configurações
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Sessão dura 7 dias


def login_required(f):
    """Decorator para rotas que exigem autenticação."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator para rotas que exigem privilégios de administrador."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        if session.get('usuario_tipo') != 'admin':
            return jsonify({'erro': 'Acesso negado'}), 403
        return f(*args, **kwargs)
    return decorated_function


# ==================== ROTAS DE AUTENTICAÇÃO ====================

@app.route('/')
def index():
    """Página inicial - redireciona baseado no tipo de usuário."""
    if 'usuario_id' in session:
        # Operador vai direto para o PDV, Admin para o dashboard
        if session.get('usuario_tipo') == 'operador':
            return redirect(url_for('pdv'))
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página e processo de login."""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        senha = data.get('senha')
        lembrar = data.get('lembrar', False)  # Checkbox "Lembrar de mim"
        
        sucesso, mensagem, usuario = auth_service.login(username, senha)
        
        if sucesso and usuario:
            # Configurar sessão
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome_completo
            session['usuario_tipo'] = usuario.tipo
            session['usuario_username'] = usuario.username
            
            # Se marcou "lembrar", torna a sessão permanente
            if lembrar:
                session.permanent = True
            
            Logger.log_operacao(
                usuario.nome_completo,
                "LOGIN_WEB",
                f"Username: {usuario.username} - Tipo: {usuario.tipo}"
            )
            
            if request.is_json:
                # Redireciona baseado no tipo
                redirect_url = url_for('pdv') if usuario.tipo == 'operador' else url_for('dashboard')
                return jsonify({
                    'sucesso': True,
                    'usuario': {
                        'id': usuario.id,
                        'nome': usuario.nome_completo,
                        'tipo': usuario.tipo
                    },
                    'redirect': redirect_url
                })
            
            # Redirect baseado no tipo de usuário
            if usuario.tipo == 'operador':
                return redirect(url_for('pdv'))
            return redirect(url_for('dashboard'))
            
            if request.is_json:
                return jsonify({
                    'sucesso': True,
                    'usuario': {
                        'id': usuario.id,
                        'nome': usuario.nome_completo,
                        'tipo': usuario.tipo
                    }
                })
            return redirect(url_for('dashboard'))
        
        if request.is_json:
            return jsonify({'sucesso': False, 'erro': mensagem}), 401
        return render_template('login.html', erro=mensagem)
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Processo de logout."""
    if 'usuario_id' in session:
        Logger.log_operacao(
            "WebApp",
            "LOGOUT",
            f"ID: {session['usuario_id']}"
        )
    session.clear()
    return redirect(url_for('login'))


# ==================== DASHBOARD ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal (admin)."""
    return render_template('dashboard.html')


# ==================== PDV (PONTO DE VENDA) ====================

@app.route('/pdv')
@login_required
def pdv():
    """Interface PDV para vendas (operadores e admins)."""
    return render_template('pdv.html')


@app.route('/api/pdv/produtos/buscar')
@login_required
def api_pdv_buscar_produtos():
    """Busca produtos para o PDV."""
    termo = request.args.get('q', '').strip()
    
    if not termo:
        return jsonify([])
    
    # Busca por código de barras ou nome
    try:
        # Tenta buscar por código de barras exato
        produto = ProdutoDAO.buscar_por_codigo_barras(termo)
        if produto:
            return jsonify([{
                'id': produto.id,
                'codigo_barras': produto.codigo_barras,
                'nome': produto.nome,
                'preco_venda': float(produto.preco_venda),
                'estoque_atual': produto.estoque_atual,
                'unidade_medida': produto.unidade_medida
            }])
        
        # Busca por nome
        produtos = ProdutoDAO.listar_ativos()
        resultados = [
            {
                'id': p.id,
                'codigo_barras': p.codigo_barras,
                'nome': p.nome,
                'preco_venda': float(p.preco_venda),
                'estoque_atual': p.estoque_atual,
                'unidade_medida': p.unidade_medida
            }
            for p in produtos
            if termo.lower() in p.nome.lower() or termo in (p.codigo_barras or '')
        ][:10]  # Limita a 10 resultados
        
        return jsonify(resultados)
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


# ==================== API - PRODUTOS ====================

@app.route('/api/produtos', methods=['GET'])
@login_required
def api_produtos_listar():
    """Lista todos os produtos."""
    produtos = ProdutoDAO.buscar_todos()
    return jsonify([{
        'id': p.id,
        'codigo_barras': p.codigo_barras,
        'nome': p.nome,
        'categoria_id': p.categoria_id,
        'preco_venda': float(p.preco_venda),
        'preco_custo': float(p.preco_custo) if p.preco_custo else 0,
        'estoque_atual': p.estoque_atual,
        'estoque_minimo': p.estoque_minimo,
        'ativo': p.ativo
    } for p in produtos])


@app.route('/api/produtos/<int:produto_id>', methods=['GET'])
@login_required
def api_produto_obter(produto_id):
    """Obtém um produto específico."""
    produto = ProdutoDAO.buscar_por_id(produto_id)
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    return jsonify({
        'id': produto.id,
        'codigo_barras': produto.codigo_barras,
        'nome': produto.nome,
        'descricao': produto.descricao,
        'categoria_id': produto.categoria_id,
        'preco_venda': float(produto.preco_venda),
        'preco_custo': float(produto.preco_custo) if produto.preco_custo else 0,
        'estoque_atual': produto.estoque_atual,
        'estoque_minimo': produto.estoque_minimo,
        'unidade_medida': produto.unidade_medida,
        'ativo': produto.ativo
    })


@app.route('/api/produtos', methods=['POST'])
@admin_required
def api_produto_criar():
    """Cria um novo produto."""
    data = request.get_json()
    
    try:
        from src.models.produto import Produto
        from decimal import Decimal
        
        produto = Produto(
            codigo_barras=data.get('codigo_barras'),
            nome=data['nome'],
            descricao=data.get('descricao'),
            categoria_id=data.get('categoria_id'),
            preco_custo=Decimal(str(data.get('preco_custo', 0))),
            preco_venda=Decimal(str(data['preco_venda'])),
            estoque_atual=data.get('estoque_atual', 0),
            estoque_minimo=data.get('estoque_minimo', 0),
            unidade_medida=data.get('unidade_medida', 'UN'),
            ativo=data.get('ativo', True)
        )
        
        produto_id = ProdutoDAO.inserir(produto)
        
        Logger.log_operacao(
            session.get('usuario_nome', 'Sistema'),
            "PRODUTO_CRIADO",
            f"ID: {produto_id} - {produto.nome}"
        )
        
        return jsonify({'sucesso': True, 'id': produto_id}), 201
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/api/produtos/<int:produto_id>', methods=['PUT'])
@admin_required
def api_produto_atualizar(produto_id):
    """Atualiza um produto existente."""
    data = request.get_json()
    produto = ProdutoDAO.buscar_por_id(produto_id)
    
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    try:
        from decimal import Decimal
        
        produto.codigo_barras = data.get('codigo_barras', produto.codigo_barras)
        produto.nome = data.get('nome', produto.nome)
        produto.descricao = data.get('descricao', produto.descricao)
        produto.categoria_id = data.get('categoria_id', produto.categoria_id)
        produto.preco_custo = Decimal(str(data.get('preco_custo', produto.preco_custo)))
        produto.preco_venda = Decimal(str(data.get('preco_venda', produto.preco_venda)))
        produto.estoque_atual = data.get('estoque_atual', produto.estoque_atual)
        produto.estoque_minimo = data.get('estoque_minimo', produto.estoque_minimo)
        produto.unidade_medida = data.get('unidade_medida', produto.unidade_medida)
        produto.ativo = data.get('ativo', produto.ativo)
        
        ProdutoDAO.atualizar(produto)
        
        Logger.log_operacao(
            session.get('usuario_nome', 'Sistema'),
            "PRODUTO_ATUALIZADO",
            f"ID: {produto_id} - {produto.nome}"
        )
        
        return jsonify({'sucesso': True})
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


# ==================== API - CATEGORIAS ====================

@app.route('/api/categorias', methods=['GET'])
@login_required
def api_categorias_listar():
    """Lista todas as categorias."""
    categorias = CategoriaDAO.buscar_todas()
    return jsonify([{
        'id': c.id,
        'nome': c.nome,
        'descricao': c.descricao,
        'ativo': c.ativo
    } for c in categorias])


# ==================== API - VENDAS ====================

@app.route('/api/vendas/resumo', methods=['GET'])
@login_required
def api_vendas_resumo():
    """Resumo de vendas do dia."""
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    if not data_inicio:
        data_inicio = datetime.now().date()
    
    total = VendaDAO.obter_total_vendas_dia(data_inicio)
    
    return jsonify({
        'data_inicio': str(data_inicio),
        'data_fim': str(data_fim) if data_fim else str(data_inicio),
        'total_vendas': float(total),
        'total_vendas_formatado': Formatters.formatar_moeda(total)
    })


# ==================== API - USUÁRIOS ====================

@app.route('/usuarios')
@admin_required
def usuarios():
    """Página de gerenciamento de usuários (admin)."""
    return render_template('usuarios.html')


@app.route('/api/usuarios', methods=['GET'])
@admin_required
def api_usuarios_listar():
    """Lista todos os usuários."""
    usuarios = UsuarioDAO.buscar_todos()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'nome_completo': u.nome_completo,
        'tipo': u.tipo,
        'ativo': u.ativo,
        'criado_em': u.criado_em.isoformat() if u.criado_em else None
    } for u in usuarios])


@app.route('/api/usuarios/<int:usuario_id>', methods=['GET'])
@admin_required
def api_usuario_obter(usuario_id):
    """Obtém um usuário específico."""
    usuario = UsuarioDAO.buscar_por_id(usuario_id)
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    return jsonify({
        'id': usuario.id,
        'username': usuario.username,
        'nome_completo': usuario.nome_completo,
        'tipo': usuario.tipo,
        'ativo': usuario.ativo,
        'criado_em': usuario.criado_em.isoformat() if usuario.criado_em else None
    })


@app.route('/api/usuarios', methods=['POST'])
@admin_required
def api_usuario_criar():
    """Cria um novo usuário."""
    try:
        data = request.get_json()
        
        from src.models.usuario import Usuario
        
        # Verifica se username já existe
        if UsuarioDAO.buscar_por_username(data['username']):
            return jsonify({'erro': 'Username já existe'}), 400
        
        usuario = Usuario(
            username=data['username'],
            nome_completo=data['nome_completo'],
            tipo=data.get('tipo', 'operador'),
            ativo=data.get('ativo', True)
        )
        usuario.set_senha(data['senha'])
        
        usuario_id = UsuarioDAO.inserir(usuario)
        
        Logger.log_operacao(
            session.get('usuario_nome', 'Sistema'),
            "USUARIO_CRIADO",
            f"ID: {usuario_id} - {usuario.username} ({usuario.tipo})"
        )
        
        return jsonify({'sucesso': True, 'id': usuario_id}), 201
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/api/usuarios/<int:usuario_id>', methods=['PUT'])
@admin_required
def api_usuario_atualizar(usuario_id):
    """Atualiza um usuário existente."""
    try:
        data = request.get_json()
        
        usuario = UsuarioDAO.buscar_por_id(usuario_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        # Não permite alterar o próprio usuário logado para inativo
        if usuario_id == session.get('usuario_id') and not data.get('ativo', True):
            return jsonify({'erro': 'Não é possível desativar o próprio usuário'}), 400
        
        usuario.nome_completo = data.get('nome_completo', usuario.nome_completo)
        usuario.tipo = data.get('tipo', usuario.tipo)
        usuario.ativo = data.get('ativo', usuario.ativo)
        
        # Atualiza senha se fornecida
        if data.get('senha'):
            usuario.set_senha(data['senha'])
        
        UsuarioDAO.atualizar(usuario)
        
        Logger.log_operacao(
            session.get('usuario_nome', 'Sistema'),
            "USUARIO_ATUALIZADO",
            f"ID: {usuario_id} - {usuario.username}"
        )
        
        return jsonify({'sucesso': True})
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/api/usuarios/<int:usuario_id>', methods=['DELETE'])
@admin_required
def api_usuario_deletar(usuario_id):
    """Desativa um usuário (soft delete)."""
    try:
        # Não permite deletar o próprio usuário
        if usuario_id == session.get('usuario_id'):
            return jsonify({'erro': 'Não é possível deletar o próprio usuário'}), 400
        
        usuario = UsuarioDAO.buscar_por_id(usuario_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        usuario.ativo = False
        UsuarioDAO.atualizar(usuario)
        
        Logger.log_operacao(
            session.get('usuario_nome', 'Sistema'),
            "USUARIO_DESATIVADO",
            f"ID: {usuario_id} - {usuario.username}"
        )
        
        return jsonify({'sucesso': True})
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


# ==================== API - CONFIGURAÇÕES ====================

@app.route('/api/configuracoes/pix', methods=['GET'])
@admin_required
def api_config_pix_obter():
    """Obtém configurações PIX do estabelecimento."""
    from src.services.config_service import PERCENTUAL_CLIENTE, PERCENTUAL_PLATAFORMA, PIX_PLATAFORMA
    
    return jsonify({
        'chave_pix_cliente': config_service.get_pix_chave_cliente(),
        'nome_beneficiario': config_service.get_pix_nome_beneficiario(),
        'cidade': config_service.get_pix_cidade(),
        'percentual_cliente_fixo': PERCENTUAL_CLIENTE,
        'percentual_plataforma_fixo': PERCENTUAL_PLATAFORMA,
        'pix_plataforma_fixo': PIX_PLATAFORMA
    })


@app.route('/api/configuracoes/pix', methods=['PUT'])
@admin_required
def api_config_pix_atualizar():
    """Atualiza configurações PIX do estabelecimento."""
    data = request.get_json()
    
    try:
        chave = data.get('chave_pix_cliente', '').strip()
        nome = data.get('nome_beneficiario', '').strip()
        cidade = data.get('cidade', '').strip()
        
        if not chave or not nome or not cidade:
            return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400
        
        config_service.set_pix_chave_cliente(chave)
        config_service.set_pix_nome_beneficiario(nome)
        config_service.set_pix_cidade(cidade)
        
        Logger.log_operacao(
            session.get('usuario_nome', 'Sistema'),
            "CONFIG_PIX",
            f"Chave: {chave[:10]}... - Nome: {nome}"
        )
        
        return jsonify({
            'sucesso': True,
            'chave_pix_cliente': chave,
            'nome_beneficiario': nome,
            'cidade': cidade
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/api/configuracoes/mercadopago', methods=['GET'])
@admin_required
def api_config_mercadopago_obter():
    """Obtém configuração do Mercado Pago (token mascarado)."""
    token = config_service.get_mercadopago_access_token()
    token_mask = f"{token[:10]}...{token[-4:]}" if len(token) > 14 else "***"
    
    return jsonify({
        'token_configurado': bool(token),
        'token_mask': token_mask if token else ''
    })


@app.route('/api/configuracoes/mercadopago', methods=['PUT'])
@admin_required
def api_config_mercadopago_atualizar():
    """Atualiza configuração do Mercado Pago."""
    data = request.get_json()
    
    try:
        token = data.get('access_token', '').strip()
        
        if not token:
            return jsonify({'erro': 'Access Token é obrigatório'}), 400
        
        config_service.set_mercadopago_access_token(token)
        
        Logger.log_operacao(
            session.get('usuario_nome', 'Sistema'),
            "CONFIG_MERCADOPAGO",
            "Access token atualizado"
        )
        
        return jsonify({
            'sucesso': True,
            'token_configurado': True
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


# ==================== API - ESTATÍSTICAS ====================

@app.route('/api/estatisticas/dashboard', methods=['GET'])
@login_required
def api_estatisticas_dashboard():
    """Estatísticas para o dashboard."""
    try:
        vendas_hoje = VendaDAO.obter_total_vendas_dia()
        produtos_estoque_baixo = ProdutoDAO.buscar_estoque_baixo()
        total_produtos = len(ProdutoDAO.buscar_todos())
        
        return jsonify({
            'vendas_hoje': {
                'valor': float(vendas_hoje),
                'formatado': Formatters.formatar_moeda(vendas_hoje)
            },
            'estoque_baixo': len(produtos_estoque_baixo),
            'total_produtos': total_produtos
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ==================== API - MERCADO PAGO WEBHOOK ====================

@app.route('/webhook/mercadopago', methods=['POST'])
def webhook_mercadopago():
    """Webhook para receber notificações do Mercado Pago."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        # Log da notificação recebida
        Logger.log_operacao("Webhook", "NOTIFICACAO_RECEBIDA", 
                          f"Tipo: {data.get('type', 'N/A')} - ID: {data.get('data', {}).get('id', 'N/A')}")
        
        # Verifica se é uma notificação de pagamento
        if data.get('type') == 'payment':
            payment_id = data.get('data', {}).get('id')
            
            if payment_id:
                # Processa em background para não bloquear o webhook
                from threading import Thread
                from src.services.mercado_pago_service import mercado_pago_service
                from src.services.pix_split_service import pix_split_service
                
                def processar_webhook_background():
                    try:
                        # Verifica status do pagamento
                        status = mercado_pago_service.verificar_status_pagamento(str(payment_id))
                        
                        if status == 'approved':
                            # Obtém dados do pagamento
                            payment_data = mercado_pago_service._obter_dados_pagamento(str(payment_id))
                            
                            if payment_data:
                                valor_total = Decimal(str(payment_data.get('transaction_amount', 0)))
                                
                                # Processa o split
                                sucesso = pix_split_service.processar_split_pagamento(
                                    payment_id_original=str(payment_id),
                                    valor_total=valor_total
                                )
                                
                                if sucesso:
                                    Logger.log_operacao("Webhook", "SPLIT_PROCESSADO_WEBHOOK", 
                                                      f"Payment ID: {payment_id} - Valor: R$ {float(valor_total):.2f}")
                                else:
                                    Logger.log_erro("Webhook", f"Falha no processamento do split via webhook: {payment_id}")
                        
                    except Exception as e:
                        Logger.log_erro("Webhook", f"Erro no processamento do webhook: {str(e)}")
                
                thread_webhook = Thread(target=processar_webhook_background, daemon=True)
                thread_webhook.start()
        
        return jsonify({'status': 'ok'}), 200
        
    except Exception as e:
        Logger.log_erro("Webhook", f"Erro no webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/produtos')
@login_required
def produtos_page():
    """Página de gestão de produtos."""
    return render_template('produtos.html', usuario=session)


@app.route('/vendas')
@login_required
def vendas_page():
    """Página de consulta de vendas."""
    return render_template('vendas.html', usuario=session)


@app.route('/configuracoes')
@admin_required
def configuracoes_page():
    """Página de configurações (apenas admin)."""
    return render_template('configuracoes.html', usuario=session)


# ==================== ERRO HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handler para erro 404."""
    if request.path.startswith('/api/'):
        return jsonify({'erro': 'Endpoint não encontrado'}), 404
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handler para erro 500."""
    if request.path.startswith('/api/'):
        return jsonify({'erro': 'Erro interno do servidor'}), 500
    return render_template('500.html'), 500


if __name__ == '__main__':
    print("=" * 60)
    print(" 🌐 PDV Web Interface")
    print("=" * 60)
    print(f" Acesse: http://localhost:5000")
    print(f" API: http://localhost:5000/api/")
    print("=" * 60)
    
    Logger.log_operacao(
        "Sistema",
        "INICIALIZACAO",
        "Servidor web iniciado"
    )
    
    app.run(debug=True, host='0.0.0.0', port=5000)
