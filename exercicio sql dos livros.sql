-- Passo 1. Crie uma tabela chamada Livros com os campos: id, titulo, autor, ano, genero, disponível.
CREATE TABLE Livros (
    id INT PRIMARY KEY,
    titulo VARCHAR(100),
    autor VARCHAR(100),
    ano INT,
    genero VARCHAR(50),
    disponivel BOOLEAN
);

-- Passo 2. Insira 5 livros fictícios (Napoleon Hill e Dale Carnegie).
INSERT INTO Livros (id, titulo, autor, ano, genero, disponivel) VALUES
(1, 'Quem Pensa Enriquece', 'Napoleon Hill', 1937, 'Autoajuda', TRUE),
(2, 'A Lei do Triunfo', 'Napoleon Hill', 1928, 'Desenvolvimento Pessoal', FALSE),
(3, 'Como Fazer Amigos e Influenciar Pessoas', 'Dale Carnegie', 1936, 'Relacionamentos', TRUE),
(4, 'Como Evitar Preocupações e Começar a Viver', 'Dale Carnegie', 1948, 'Desenvolvimento Pessoal', TRUE),
(5, 'Mais Esperto que o Diabo', 'Napoleon Hill', 2011, 'Filosofia de Vida', TRUE);

-- Passo 3. Selecione todos os livros disponíveis.
SELECT * FROM Livros 
WHERE disponivel = TRUE;

-- Passo 4. Atualize a disponibilidade de 1 livro (Mudando 'A Lei do Triunfo' para disponível = TRUE).
UPDATE Livros 
SET disponivel = TRUE 
WHERE id = 2;

-- Passo 5. Liste os livros do mais recente para o mais antigo.
SELECT * FROM Livros 
ORDER BY ano DESC;

-- Passo 6. Delete um livro com ano anterior a 1940 (Deletará os livros de 1928, 1936 e 1937).
DELETE FROM Livros 
WHERE ano < 1940;

-- Passo 7. Apague e recrie a tabela Livros.
DROP TABLE IF EXISTS Livros;

CREATE TABLE Livros (
    id INT PRIMARY KEY,
    titulo VARCHAR(100),
    autor VARCHAR(100),
    ano INT,
    genero VARCHAR(50),
    disponivel BOOLEAN
);