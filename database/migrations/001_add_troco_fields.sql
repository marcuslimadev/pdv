-- Migração 001: Adicionar campos valor_pago e troco na tabela pagamentos
-- Data: 2024
-- Descrição: Permite registrar o valor pago pelo cliente e o troco calculado

USE pdv_sistema;

-- Adiciona coluna valor_pago (valor que o cliente efetivamente pagou)
ALTER TABLE pagamentos 
ADD COLUMN valor_pago DECIMAL(10,2) NULL AFTER dados_pix,
ADD COLUMN troco DECIMAL(10,2) DEFAULT 0.00 AFTER valor_pago;

-- Atualiza registros existentes: valor_pago = valor (retrocompatibilidade)
UPDATE pagamentos 
SET valor_pago = valor, troco = 0.00 
WHERE valor_pago IS NULL;

-- Opcional: tornar valor_pago NOT NULL após atualização
-- ALTER TABLE pagamentos MODIFY COLUMN valor_pago DECIMAL(10,2) NOT NULL;

-- Verificação
SELECT 'Migração 001 aplicada com sucesso!' as status;
SELECT COUNT(*) as total_pagamentos, 
       COUNT(valor_pago) as com_valor_pago,
       COUNT(troco) as com_troco
FROM pagamentos;
