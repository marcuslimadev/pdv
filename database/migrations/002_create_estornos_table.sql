-- Migração 002: Criar tabela de estornos
-- Data: 2024-10-28
-- Descrição: Permite registrar estornos de vendas com motivo e reversão de estoque

USE pdv_sistema;

-- Cria tabela de estornos
CREATE TABLE IF NOT EXISTS estornos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venda_id INT NOT NULL,
    usuario_id INT NOT NULL COMMENT 'Admin que autorizou o estorno',
    data_estorno DATETIME DEFAULT CURRENT_TIMESTAMP,
    motivo TEXT NOT NULL,
    valor_estornado DECIMAL(10,2) NOT NULL,
    observacoes TEXT,
    FOREIGN KEY (venda_id) REFERENCES vendas(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    INDEX idx_venda (venda_id),
    INDEX idx_usuario (usuario_id),
    INDEX idx_data (data_estorno)
) ENGINE=InnoDB COMMENT='Registros de estornos de vendas';

-- Verificação
SELECT 'Migração 002 aplicada com sucesso!' as status;
SHOW CREATE TABLE estornos;
