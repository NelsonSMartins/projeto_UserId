import pandas as pd
import json

# 1. Ler o CSV
df = pd.read_csv('SDW2023.csv')
user_ids = df['UserID'].tolist()
print(f"IDs encontrados no CSV: {user_ids}")

# 2. Carregar dados do cadastro.json
try:
    with open('cadastro.json', 'r', encoding='utf-8') as file:
        all_users_data = json.load(file)
except FileNotFoundError:
    print("Arquivo cadastro.json não encontrado. Criando nova lista.")
    all_users_data = []
except json.JSONDecodeError:
    print("Erro ao ler cadastro.json. Iniciando com lista vazia.")
    all_users_data = []

# 3. Função para gerar mensagem personalizada (sem API)
def generate_ai_news(user):
    mensagens = [
        f"Olá {user['name']}! Invista hoje para garantir seu amanhã.",
        f"{user['name']}, seu futuro financeiro começa agora. Invista!",
        f"Querido {user['name']}, pequenos investimentos geram grandes resultados.",
        f"{user['name']}, a jornada para sua liberdade financeira começa aqui.",
        f"Olá {user['name']}! Seu dinheiro pode trabalhar para você. Invista!",
        f"{user['name']}, não espere para investir. O melhor momento é agora.",
        f"Caro {user['name']}, diversifique e multiplique seus rendimentos.",
        f"{user['name']}, cada investimento é um passo rumo à estabilidade."
    ]
    
    # Usa o ID do usuário para escolher uma mensagem consistente
    import hashlib
    user_hash = int(hashlib.md5(str(user.get('id', 0)).encode()).hexdigest(), 16)
    mensagem = mensagens[user_hash % len(mensagens)]
    
    # Garante que tenha no máximo 100 caracteres
    return mensagem[:100]

# 4. Processar cada usuário do CSV
usuarios_processados = []

for user_id in user_ids:
    # Buscar usuário no cadastro.json
    usuario = None
    for user in all_users_data:
        if user.get('id') == user_id:
            usuario = user.copy()  # Faz uma cópia para não modificar o original
            break
    
    # Se não encontrou, criar um novo usuário básico
    if not usuario:
        usuario = {
            'id': user_id,
            'name': f'Usuário_{user_id}',
            'news': []
        }
        print(f"Usuário ID {user_id} não encontrado no JSON. Criando novo.")
    
    # Gerar mensagem personalizada
    try:
        news = generate_ai_news(usuario)
        print(f"Para {usuario['name']}: {news}")
        
        # Adicionar a notícia
        if 'news' not in usuario:
            usuario['news'] = []
        
        usuario['news'].append({
            "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
            "description": news
        })
        
        usuarios_processados.append(usuario)
        
    except Exception as e:
        print(f"Erro ao processar usuário {user_id}: {e}")

# 5. Atualizar/Adicionar usuários no cadastro.json
for usuario in usuarios_processados:
    usuario_encontrado = False
    
    for i, existing_user in enumerate(all_users_data):
        if existing_user.get('id') == usuario.get('id'):
            all_users_data[i] = usuario
            usuario_encontrado = True
            break
    
    if not usuario_encontrado:
        all_users_data.append(usuario)

# 6. Salvar o arquivo JSON atualizado
with open('cadastro.json', 'w', encoding='utf-8') as file:
    json.dump(all_users_data, file, ensure_ascii=False, indent=2)

# 7. Atualizar o CSV com informações do processamento
# Adicionar coluna com status do processamento
df['Processado'] = 'Sim'
df['Data_Processamento'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')

# Salvar o CSV atualizado
df.to_csv('SDW2023_atualizado.csv', index=False)

# 8. Criar um resumo do processamento
resumo_df = pd.DataFrame({
    'ID': [u['id'] for u in usuarios_processados],
    'Nome': [u['name'] for u in usuarios_processados],
    'Mensagem': [u['news'][-1]['description'] if u.get('news') else 'Sem mensagem' 
                 for u in usuarios_processados],
    'Total_Mensagens': [len(u.get('news', [])) for u in usuarios_processados]
})

print("\n" + "="*60)
print("RESUMO DO PROCESSAMENTO")
print("="*60)
print(f"Total de IDs no CSV: {len(user_ids)}")
print(f"Usuários processados: {len(usuarios_processados)}")
print(f"Novos usuários criados: {len([u for u in usuarios_processados if 'Usuário_' in u['name']])}")
print("\nDetalhes:")
print(resumo_df.to_string(index=False))

# Salvar resumo em CSV
resumo_df.to_csv('resumo_processamento.csv', index=False)
print(f"\nResumo salvo em 'resumo_processamento.csv'")
print("CSV atualizado salvo como 'SDW2023_atualizado.csv'")
print("JSON atualizado salvo como 'cadastro.json'")
