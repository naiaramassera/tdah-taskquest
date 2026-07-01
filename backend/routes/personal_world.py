from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.core.dependencies import get_current_user
from backend.models.world import World
from backend.models.routine_task import RoutineTask

router = APIRouter(tags=["Personal World"])

# Atividades sugeridas por categoria para o mundo pessoal
PERSONAL_CATEGORIES = [
    {
        "id": "casa",
        "name": "Casa",
        "icon": "🏠",
        "color": "#22C55E",
        "activities": [
            {"title": "Arrumar o quarto", "description": "Organizar roupas, cama e superfícies", "difficulty": 1, "minutes": 20},
            {"title": "Lavar a louça", "description": "Lavar e secar todos os utensílios", "difficulty": 1, "minutes": 15},
            {"title": "Limpar o banheiro", "description": "Limpar vaso, pia e chão", "difficulty": 2, "minutes": 25},
            {"title": "Varrer e passar pano", "description": "Limpar o chão da casa", "difficulty": 2, "minutes": 30},
            {"title": "Lavar roupa", "description": "Lavar, secar e dobrar as roupas", "difficulty": 2, "minutes": 45},
            {"title": "Organizar a geladeira", "description": "Limpar e reorganizar alimentos", "difficulty": 1, "minutes": 20},
            {"title": "Tirar o lixo", "description": "Recolher e levar o lixo para fora", "difficulty": 1, "minutes": 10},
            {"title": "Limpar a cozinha", "description": "Superfícies, fogão e pia", "difficulty": 2, "minutes": 25},
            {"title": "Organizar guarda-roupa", "description": "Dobrar e organizar as roupas por tipo", "difficulty": 2, "minutes": 40},
            {"title": "Fazer as compras", "description": "Ir ao mercado com lista pronta", "difficulty": 2, "minutes": 60},
        ],
    },
    {
        "id": "saude",
        "name": "Saúde e Bem-estar",
        "icon": "🏃",
        "color": "#EF4444",
        "activities": [
            {"title": "Fazer exercício", "description": "Caminhada, academia ou treino em casa", "difficulty": 2, "minutes": 45},
            {"title": "Beber 2L de água", "description": "Manter hidratação ao longo do dia", "difficulty": 1, "minutes": 0},
            {"title": "Meditar", "description": "10 minutos de meditação ou respiração", "difficulty": 1, "minutes": 10},
            {"title": "Alongamento", "description": "Série de alongamentos para o corpo", "difficulty": 1, "minutes": 15},
            {"title": "Dormir no horário", "description": "Ir para a cama no horário planejado", "difficulty": 2, "minutes": 0},
            {"title": "Cozinhar refeição saudável", "description": "Preparar uma refeição balanceada", "difficulty": 2, "minutes": 40},
            {"title": "Tomar medicamento", "description": "Tomar remédio ou suplemento no horário", "difficulty": 1, "minutes": 5},
            {"title": "Consulta médica", "description": "Ir à consulta ou exame agendado", "difficulty": 3, "minutes": 90},
        ],
    },
    {
        "id": "estudos",
        "name": "Estudos",
        "icon": "📖",
        "color": "#3B82F6",
        "activities": [
            {"title": "Estudar conteúdo", "description": "Sessão de estudos focada", "difficulty": 2, "minutes": 45},
            {"title": "Ler livro", "description": "Leitura de pelo menos 20 páginas", "difficulty": 1, "minutes": 30},
            {"title": "Assistir aula", "description": "Assistir aula online ou gravada", "difficulty": 1, "minutes": 60},
            {"title": "Fazer exercícios", "description": "Resolver exercícios ou lista de questões", "difficulty": 2, "minutes": 45},
            {"title": "Revisar anotações", "description": "Reler e organizar anotações da semana", "difficulty": 1, "minutes": 20},
            {"title": "Pesquisar tema novo", "description": "Explorar conteúdo de interesse", "difficulty": 1, "minutes": 30},
            {"title": "Fazer resumo", "description": "Escrever resumo de conteúdo estudado", "difficulty": 2, "minutes": 30},
            {"title": "Praticar idioma", "description": "Exercícios ou conversação no idioma", "difficulty": 2, "minutes": 30},
        ],
    },
    {
        "id": "financas",
        "name": "Finanças",
        "icon": "💰",
        "color": "#F59E0B",
        "activities": [
            {"title": "Pagar conta", "description": "Pagar boleto ou fatura do mês", "difficulty": 1, "minutes": 10},
            {"title": "Registrar gastos", "description": "Anotar despesas do dia no controle", "difficulty": 1, "minutes": 10},
            {"title": "Revisar orçamento", "description": "Verificar entradas e saídas do mês", "difficulty": 2, "minutes": 20},
            {"title": "Pesquisar preço", "description": "Comparar preços antes de comprar algo", "difficulty": 1, "minutes": 15},
            {"title": "Guardar dinheiro", "description": "Separar valor para poupança ou meta", "difficulty": 2, "minutes": 5},
            {"title": "Organizar documentos", "description": "Organizar comprovantes e recibos", "difficulty": 1, "minutes": 20},
        ],
    },
    {
        "id": "familia",
        "name": "Família e Social",
        "icon": "👨‍👩‍👧",
        "color": "#8B5CF6",
        "activities": [
            {"title": "Ligar para família", "description": "Ligar para pai, mãe ou parente", "difficulty": 1, "minutes": 15},
            {"title": "Responder mensagens", "description": "Responder amigos e familiares pendentes", "difficulty": 1, "minutes": 15},
            {"title": "Tempo de qualidade", "description": "Momento com família ou amigos", "difficulty": 1, "minutes": 60},
            {"title": "Fazer planos sociais", "description": "Organizar encontro ou atividade com pessoas", "difficulty": 1, "minutes": 15},
            {"title": "Cuidar de pet", "description": "Alimentar, passear ou brincar com o animal", "difficulty": 1, "minutes": 20},
            {"title": "Ajudar alguém", "description": "Oferecer ajuda a familiar ou amigo", "difficulty": 1, "minutes": 30},
        ],
    },
    {
        "id": "lazer",
        "name": "Lazer e Criatividade",
        "icon": "🎨",
        "color": "#EC4899",
        "activities": [
            {"title": "Hobby criativo", "description": "Desenho, escrita, música ou artesanato", "difficulty": 1, "minutes": 45},
            {"title": "Assistir série ou filme", "description": "Momento de entretenimento planejado", "difficulty": 1, "minutes": 60},
            {"title": "Sair para caminhar", "description": "Passeio ao ar livre sem objetivo", "difficulty": 1, "minutes": 30},
            {"title": "Jogar", "description": "Jogo favorito por tempo limitado", "difficulty": 1, "minutes": 45},
            {"title": "Ouvir música", "description": "Playlist favorita ou descobrir algo novo", "difficulty": 1, "minutes": 20},
        ],
    },
]


router_personal = APIRouter(tags=["Personal World"])


@router_personal.get("/categories")
def get_personal_categories():
    return [
        {
            "id": cat["id"],
            "name": cat["name"],
            "icon": cat["icon"],
            "color": cat["color"],
            "activity_count": len(cat["activities"]),
        }
        for cat in PERSONAL_CATEGORIES
    ]


@router_personal.get("/categories/{category_id}")
def get_category_activities(category_id: str):
    cat = next((c for c in PERSONAL_CATEGORIES if c["id"] == category_id), None)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return cat


@router_personal.post("/setup")
def setup_personal_world(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    existing = db.query(World).filter_by(user_id=current_user.id, world_type="personal").first()
    if existing:
        return {"world_id": existing.id, "message": "Mundo pessoal já existe"}

    world = World(
        user_id=current_user.id,
        name="Vida Pessoal",
        icon="🏠",
        color="#22C55E",
        description="Rotinas do dia a dia",
        world_type="personal",
    )
    db.add(world)
    db.commit()
    db.refresh(world)
    return {"world_id": world.id, "message": "Mundo pessoal criado"}


@router_personal.post("/add-activities")
def add_personal_activities(
    category_id: str,
    activity_ids: str,  # "0,1,3" — índices separados por vírgula
    world_id: int = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    cat = next((c for c in PERSONAL_CATEGORIES if c["id"] == category_id), None)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    # Garantir que o mundo pessoal existe
    if world_id:
        world = db.query(World).filter_by(id=world_id, user_id=current_user.id).first()
    else:
        world = db.query(World).filter_by(user_id=current_user.id, world_type="personal").first()

    if not world:
        world = World(
            user_id=current_user.id,
            name="Vida Pessoal",
            icon="🏠",
            color="#22C55E",
            description="Rotinas do dia a dia",
            world_type="personal",
        )
        db.add(world)
        db.commit()
        db.refresh(world)

    indices = [int(i) for i in activity_ids.split(",") if i.strip().isdigit()]
    added = []

    for idx in indices:
        if idx >= len(cat["activities"]):
            continue
        act = cat["activities"][idx]
        coin_reward = 10 + (act["difficulty"] - 1) * 5
        xp_reward = 15 + (act["difficulty"] - 1) * 10
        routine = RoutineTask(
            world_id=world.id,
            title=act["title"],
            description=act["description"],
            difficulty=act["difficulty"],
            time_limit_minutes=act["minutes"] if act["minutes"] > 0 else None,
            coin_reward=coin_reward,
            xp_reward=xp_reward,
        )
        db.add(routine)
        added.append(act["title"])

    db.commit()
    return {"added": added, "world_id": world.id}
