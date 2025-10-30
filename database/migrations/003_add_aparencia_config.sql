-- ========================================
-- MIGRAÇÃO: Criar tabela de configurações de aparência
-- ========================================

USE pdv_sistema;

-- Criar tabela específica para aparência
CREATE TABLE IF NOT EXISTS aparencia_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cor_primaria VARCHAR(7) DEFAULT '#6C5CE7',
    cor_secundaria VARCHAR(7) DEFAULT '#00B894',
    cor_destaque VARCHAR(7) DEFAULT '#FDCB6E',
    cor_perigo VARCHAR(7) DEFAULT '#D63031',
    cor_info VARCHAR(7) DEFAULT '#74B9FF',
    cor_aviso VARCHAR(7) DEFAULT '#FFEAA7',
    cor_texto_primario VARCHAR(7) DEFAULT '#2D3436',
    cor_texto_secundario VARCHAR(7) DEFAULT '#636E72',
    cor_fundo VARCHAR(7) DEFAULT '#F5F6FA',
    fonte_principal VARCHAR(100) DEFAULT 'Segoe UI',
    tamanho_fonte_pequeno INT DEFAULT 8,
    tamanho_fonte_normal INT DEFAULT 10,
    tamanho_fonte_medio INT DEFAULT 11,
    tamanho_fonte_grande INT DEFAULT 13,
    tamanho_fonte_xlarge INT DEFAULT 16,
    tamanho_fonte_xxlarge INT DEFAULT 24,
    tamanho_fonte_huge INT DEFAULT 32,
    borda_arredondada INT DEFAULT 4,
    logotipo_path VARCHAR(500) DEFAULT NULL,
    mostrar_logotipo BOOLEAN DEFAULT FALSE,
    logotipo_largura INT DEFAULT 150,
    logotipo_altura INT DEFAULT 50,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Inserir configuração padrão
INSERT INTO aparencia_config (id) 
SELECT 1 WHERE NOT EXISTS (SELECT 1 FROM aparencia_config WHERE id = 1);

