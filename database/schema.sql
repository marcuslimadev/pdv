-- ========================================
-- SISTEMA PDV - SCHEMA DO BANCO DE DADOS
-- ========================================

-- Criar banco de dados
DROP DATABASE IF EXISTS pdv_sistema;
CREATE DATABASE pdv_sistema CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE pdv_sistema;

-- ========================================
-- TABELA: categorias
-- ========================================
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nome (nome),
    INDEX idx_ativo (ativo)
) ENGINE=InnoDB;

-- ========================================
-- TABELA: produtos
-- ========================================
CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_barras VARCHAR(50) UNIQUE,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT,
    categoria_id INT,
    preco_custo DECIMAL(10,2) DEFAULT 0.00,
    preco_venda DECIMAL(10,2) NOT NULL,
    estoque_atual INT DEFAULT 0,
    estoque_minimo INT DEFAULT 0,
    unidade_medida VARCHAR(20) DEFAULT 'UN',
    ativo BOOLEAN DEFAULT TRUE,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL,
    INDEX idx_codigo_barras (codigo_barras),
    INDEX idx_nome (nome),
    INDEX idx_categoria (categoria_id),
    INDEX idx_ativo (ativo)
) ENGINE=InnoDB;

-- ========================================
-- TABELA: usuarios
-- ========================================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    nome_completo VARCHAR(200) NOT NULL,
    tipo ENUM('admin', 'operador') DEFAULT 'operador',
    ativo BOOLEAN DEFAULT TRUE,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultimo_acesso DATETIME,
    INDEX idx_username (username),
    INDEX idx_tipo (tipo),
    INDEX idx_ativo (ativo)
) ENGINE=InnoDB;

-- ========================================
-- TABELA: caixa
-- ========================================
CREATE TABLE caixa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_fechamento DATETIME,
    valor_abertura DECIMAL(10,2) DEFAULT 0.00,
    valor_fechamento DECIMAL(10,2),
    status ENUM('aberto', 'fechado') DEFAULT 'aberto',
    observacoes TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    INDEX idx_usuario (usuario_id),
    INDEX idx_status (status),
    INDEX idx_data_abertura (data_abertura)
) ENGINE=InnoDB;

-- ========================================
-- TABELA: vendas
-- ========================================
CREATE TABLE vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_venda VARCHAR(20) UNIQUE NOT NULL,
    usuario_id INT NOT NULL,
    caixa_id INT,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    subtotal DECIMAL(10,2) DEFAULT 0.00,
    desconto DECIMAL(10,2) DEFAULT 0.00,
    total DECIMAL(10,2) NOT NULL,
    status ENUM('aberta', 'finalizada', 'cancelada') DEFAULT 'aberta',
    observacoes TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (caixa_id) REFERENCES caixa(id) ON DELETE SET NULL,
    INDEX idx_numero_venda (numero_venda),
    INDEX idx_usuario (usuario_id),
    INDEX idx_caixa (caixa_id),
    INDEX idx_data_hora (data_hora),
    INDEX idx_status (status)
) ENGINE=InnoDB;

-- ========================================
-- TABELA: itens_venda
-- ========================================
CREATE TABLE itens_venda (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venda_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade DECIMAL(10,3) NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    desconto DECIMAL(10,2) DEFAULT 0.00,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (venda_id) REFERENCES vendas(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
    INDEX idx_venda (venda_id),
    INDEX idx_produto (produto_id)
) ENGINE=InnoDB;

-- ========================================
-- TABELA: pagamentos
-- ========================================
CREATE TABLE pagamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venda_id INT NOT NULL,
    forma_pagamento ENUM('dinheiro', 'debito', 'credito', 'pix') NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    numero_parcelas INT DEFAULT 1,
    status ENUM('pendente', 'aprovado', 'recusado') DEFAULT 'pendente',
    nsu VARCHAR(50),
    codigo_autorizacao VARCHAR(50),
    dados_pix TEXT,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (venda_id) REFERENCES vendas(id) ON DELETE CASCADE,
    INDEX idx_venda (venda_id),
    INDEX idx_forma_pagamento (forma_pagamento),
    INDEX idx_status (status),
    INDEX idx_data_hora (data_hora)
) ENGINE=InnoDB;

-- ========================================
-- TABELA: movimentacoes_estoque
-- ========================================
CREATE TABLE movimentacoes_estoque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT NOT NULL,
    tipo ENUM('entrada', 'saida', 'ajuste') NOT NULL,
    quantidade DECIMAL(10,3) NOT NULL,
    motivo VARCHAR(200),
    usuario_id INT NOT NULL,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    INDEX idx_produto (produto_id),
    INDEX idx_tipo (tipo),
    INDEX idx_usuario (usuario_id),
    INDEX idx_data_hora (data_hora)
) ENGINE=InnoDB;

-- ========================================
-- DADOS INICIAIS
-- ========================================

-- Inserir usuário administrador padrão
-- Senha: admin123 (hash bcrypt)
INSERT INTO usuarios (username, senha_hash, nome_completo, tipo, ativo) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lW3qGXbG5sFi', 'Administrador', 'admin', TRUE);

-- Inserir usuário operador padrão
-- Senha: operador123 (hash bcrypt)
INSERT INTO usuarios (username, senha_hash, nome_completo, tipo, ativo) VALUES
('operador', '$2b$12$92y0p.4gKqKVZnGj6Y/oT.Xr1X3KHhT5K5rQZT9vKqGkKZkZnZKqO', 'Operador de Caixa', 'operador', TRUE);

-- Inserir categorias de exemplo
INSERT INTO categorias (nome, descricao, ativo) VALUES
('Alimentos', 'Produtos alimentícios em geral', TRUE),
('Bebidas', 'Bebidas diversas', TRUE),
('Limpeza', 'Produtos de limpeza', TRUE),
('Higiene', 'Produtos de higiene pessoal', TRUE),
('Mercearia', 'Produtos de mercearia', TRUE);

-- Inserir produtos de exemplo
INSERT INTO produtos (codigo_barras, nome, descricao, categoria_id, preco_custo, preco_venda, estoque_atual, estoque_minimo, unidade_medida, ativo) VALUES
('7891234567890', 'Arroz Branco 1kg', 'Arroz tipo 1', 5, 3.50, 5.99, 50, 10, 'UN', TRUE),
('7891234567891', 'Feijão Preto 1kg', 'Feijão tipo 1', 5, 4.00, 6.99, 40, 10, 'UN', TRUE),
('7891234567892', 'Açúcar 1kg', 'Açúcar cristal', 5, 2.50, 4.49, 30, 10, 'UN', TRUE),
('7891234567893', 'Café 500g', 'Café torrado e moído', 1, 8.00, 12.99, 25, 5, 'UN', TRUE),
('7891234567894', 'Leite Integral 1L', 'Leite longa vida', 1, 3.00, 4.99, 60, 15, 'UN', TRUE),
('7891234567895', 'Refrigerante Cola 2L', 'Refrigerante sabor cola', 2, 4.50, 7.99, 35, 10, 'UN', TRUE),
('7891234567896', 'Água Mineral 1.5L', 'Água mineral sem gás', 2, 1.50, 2.99, 100, 20, 'UN', TRUE),
('7891234567897', 'Detergente Líquido 500ml', 'Detergente neutro', 3, 1.80, 2.99, 45, 10, 'UN', TRUE),
('7891234567898', 'Sabão em Pó 1kg', 'Sabão em pó para roupas', 3, 6.00, 9.99, 30, 8, 'UN', TRUE),
('7891234567899', 'Sabonete 90g', 'Sabonete em barra', 4, 1.20, 2.49, 80, 20, 'UN', TRUE);

-- ========================================
-- VIEWS ÚTEIS
-- ========================================

-- View para produtos com baixo estoque
CREATE VIEW produtos_estoque_baixo AS
SELECT 
    p.id,
    p.codigo_barras,
    p.nome,
    c.nome AS categoria,
    p.estoque_atual,
    p.estoque_minimo,
    p.preco_venda
FROM produtos p
LEFT JOIN categorias c ON p.categoria_id = c.id
WHERE p.estoque_atual <= p.estoque_minimo
AND p.ativo = TRUE;

-- View para resumo de vendas diárias
CREATE VIEW resumo_vendas_diarias AS
SELECT 
    DATE(v.data_hora) AS data,
    COUNT(v.id) AS total_vendas,
    SUM(v.total) AS valor_total,
    AVG(v.total) AS ticket_medio
FROM vendas v
WHERE v.status = 'finalizada'
GROUP BY DATE(v.data_hora);

-- View para produtos mais vendidos
CREATE VIEW produtos_mais_vendidos AS
SELECT 
    p.id,
    p.nome,
    c.nome AS categoria,
    SUM(iv.quantidade) AS quantidade_vendida,
    SUM(iv.subtotal) AS valor_total
FROM itens_venda iv
JOIN produtos p ON iv.produto_id = p.id
LEFT JOIN categorias c ON p.categoria_id = c.id
JOIN vendas v ON iv.venda_id = v.id
WHERE v.status = 'finalizada'
GROUP BY p.id, p.nome, c.nome
ORDER BY quantidade_vendida DESC;

-- ========================================
-- TRIGGERS
-- ========================================

-- Trigger para atualizar estoque após venda
DELIMITER $$

CREATE TRIGGER tr_atualizar_estoque_venda
AFTER INSERT ON itens_venda
FOR EACH ROW
BEGIN
    UPDATE produtos 
    SET estoque_atual = estoque_atual - NEW.quantidade
    WHERE id = NEW.produto_id;
    
    -- Registrar movimentação de estoque
    INSERT INTO movimentacoes_estoque (produto_id, tipo, quantidade, motivo, usuario_id)
    SELECT NEW.produto_id, 'saida', NEW.quantidade, 
           CONCAT('Venda #', v.numero_venda), v.usuario_id
    FROM vendas v WHERE v.id = NEW.venda_id;
END$$

DELIMITER ;

-- ========================================
-- FIM DO SCHEMA
-- ========================================
