"""
Seed de profissões e missões profissionais.
Execute: python -m backend.seed_professions
"""
from backend.database.base import Base
from backend.database.session import SessionLocal, engine
from backend.models.profession import Profession
from backend.models.profession_mission import ProfessionMission

Base.metadata.create_all(bind=engine)

PROFESSIONS = [
    # ── SAÚDE ──────────────────────────────────────────────────────────
    {
        "name": "Médico(a)",
        "icon": "🩺",
        "category": "saude",
        "description": "Diagnóstico, tratamento e cuidado dos pacientes.",
        "missions": [
            ("Fazer rondas no hospital", "Visitar todos os pacientes internados", 2, 25, 30, 40),
            ("Revisar prontuários", "Atualizar registros dos pacientes do dia", 1, 15, 20, 20),
            ("Atender consultas", "Realizar atendimentos ambulatoriais", 2, 20, 30, 45),
            ("Atualizar prescrições", "Revisar e ajustar medicamentos", 2, 20, 25, 30),
            ("Estudar caso clínico", "Pesquisar sobre condição específica de um paciente", 3, 35, 45, 60),
            ("Completar relatório de alta", "Finalizar documentação de pacientes com alta", 2, 20, 25, 30),
            ("Participar de reunião de equipe", "Alinhamento com enfermagem e demais profissionais", 1, 15, 20, 45),
        ],
    },
    {
        "name": "Psicólogo(a)",
        "icon": "🧠",
        "category": "saude",
        "description": "Saúde mental, avaliação psicológica e terapia.",
        "missions": [
            ("Atender sessão terapêutica", "Conduzir sessão de 50 minutos com paciente", 2, 20, 30, 60),
            ("Escrever evolução do paciente", "Registrar notas clínicas após atendimento", 1, 15, 20, 15),
            ("Estudar caso clínico", "Preparar intervenção para próxima sessão", 2, 25, 30, 45),
            ("Supervisão clínica", "Discutir caso com supervisor ou colega", 2, 20, 25, 60),
            ("Elaborar plano terapêutico", "Definir objetivos e estratégias para paciente", 3, 30, 40, 60),
            ("Fazer avaliação psicológica", "Aplicar e interpretar testes psicológicos", 3, 35, 45, 90),
            ("Atualizar agenda", "Confirmar consultas e organizar semana", 1, 10, 15, 15),
        ],
    },
    {
        "name": "Biomédico(a)",
        "icon": "🔬",
        "category": "saude",
        "description": "Análises laboratoriais, diagnóstico e pesquisa.",
        "missions": [
            ("Realizar análise laboratorial", "Executar exames de rotina do laboratório", 2, 20, 30, 45),
            ("Calibrar equipamentos", "Verificar e calibrar aparelhos do laboratório", 2, 20, 25, 30),
            ("Registrar resultados", "Lançar laudos no sistema", 1, 15, 20, 20),
            ("Estudar protocolo técnico", "Revisar procedimento ou norma técnica", 2, 20, 25, 40),
            ("Controle de qualidade", "Verificar amostras controle e validar lote", 3, 30, 40, 60),
            ("Organizar estoque de reagentes", "Conferir validades e repor insumos", 1, 10, 15, 20),
        ],
    },
    {
        "name": "Farmacêutico(a)",
        "icon": "💊",
        "category": "saude",
        "description": "Dispensação, orientação e controle de medicamentos.",
        "missions": [
            ("Verificar estoque de medicamentos", "Conferir validades e quantidade em estoque", 1, 15, 20, 20),
            ("Atender prescrição médica", "Dispensar medicamentos com orientação", 2, 20, 25, 20),
            ("Orientar paciente sobre medicação", "Explicar posologia e efeitos colaterais", 2, 20, 25, 15),
            ("Revisar interações medicamentosas", "Checar compatibilidade de prescrições", 3, 30, 40, 30),
            ("Atualizar cadastro de produtos", "Manter sistema de gestão atualizado", 1, 10, 15, 20),
            ("Fazer pedido de compra", "Repor medicamentos com baixo estoque", 2, 20, 25, 30),
        ],
    },
    {
        "name": "Enfermeiro(a)",
        "icon": "🩹",
        "category": "saude",
        "description": "Cuidado direto ao paciente, procedimentos e gestão assistencial.",
        "missions": [
            ("Fazer rondas nos leitos", "Verificar condição de todos os pacientes", 2, 20, 30, 40),
            ("Aplicar medicação", "Administrar medicamentos conforme prescrição", 2, 20, 25, 30),
            ("Registrar sinais vitais", "Aferir e documentar PA, temp, FC dos pacientes", 1, 15, 20, 30),
            ("Fazer curativo", "Realizar troca de curativo em pacientes", 2, 20, 25, 20),
            ("Checar prontuário", "Revisar prescrições e pendências do turno", 1, 15, 20, 20),
            ("Passagem de plantão", "Transmitir informações ao próximo turno", 2, 20, 25, 30),
            ("Cateterismo ou coleta", "Realizar procedimento técnico prescrito", 3, 30, 35, 30),
        ],
    },
    {
        "name": "Esteticista",
        "icon": "💆",
        "category": "saude",
        "description": "Estética facial, corporal e bem-estar.",
        "missions": [
            ("Atender cliente", "Realizar atendimento agendado", 2, 20, 25, 60),
            ("Fazer protocolo facial", "Executar limpeza ou tratamento facial completo", 2, 25, 30, 60),
            ("Fazer protocolo corporal", "Drenagem, massagem ou modelagem corporal", 2, 25, 30, 60),
            ("Estudar nova técnica", "Pesquisar ou praticar técnica estética nova", 2, 20, 25, 45),
            ("Organizar agenda do dia", "Confirmar atendimentos e preparar materiais", 1, 10, 15, 15),
            ("Esterilizar materiais", "Higienizar e organizar equipamentos", 1, 10, 15, 20),
        ],
    },
    # ── NEGÓCIOS ───────────────────────────────────────────────────────
    {
        "name": "Administrador(a)",
        "icon": "📊",
        "category": "negocios",
        "description": "Gestão, planejamento e resultados organizacionais.",
        "missions": [
            ("Revisar metas da semana", "Acompanhar indicadores e resultados", 2, 20, 30, 30),
            ("Conduzir reunião de equipe", "Alinhamento semanal com o time", 2, 25, 30, 60),
            ("Analisar relatório financeiro", "Revisar DRE ou fluxo de caixa", 3, 30, 40, 45),
            ("Elaborar planejamento", "Definir estratégias para próximo período", 3, 35, 45, 60),
            ("Responder e-mails estratégicos", "Tratar comunicações importantes do dia", 1, 15, 20, 20),
            ("Delegar tarefas", "Distribuir responsabilidades para a equipe", 2, 20, 25, 20),
        ],
    },
    {
        "name": "Contador(a)",
        "icon": "🧾",
        "category": "negocios",
        "description": "Contabilidade, tributos e saúde financeira.",
        "missions": [
            ("Fechar balancete mensal", "Conciliar contas e fechar período contábil", 3, 35, 45, 90),
            ("Declarar tributos", "Calcular e enviar obrigações fiscais", 3, 30, 40, 60),
            ("Revisar lançamentos contábeis", "Verificar lançamentos do dia no sistema", 2, 20, 25, 30),
            ("Atender cliente", "Reunião ou call de consultoria contábil", 2, 20, 30, 45),
            ("Conciliar contas bancárias", "Comparar extrato com sistema contábil", 2, 20, 25, 30),
            ("Atualizar legislação", "Estudar nova norma ou lei tributária", 2, 20, 25, 40),
        ],
    },
    {
        "name": "Advogado(a)",
        "icon": "⚖️",
        "category": "negocios",
        "description": "Direito, processos, contratos e consultoria jurídica.",
        "missions": [
            ("Redigir petição", "Elaborar documento jurídico para processo", 3, 35, 45, 90),
            ("Analisar processo", "Revisar andamento de processo no tribunal", 2, 25, 30, 60),
            ("Reunião com cliente", "Consulta jurídica ou atualização de caso", 2, 20, 30, 45),
            ("Estudar jurisprudência", "Pesquisar precedentes para embasar tese", 3, 30, 40, 60),
            ("Revisar contrato", "Analisar e ajustar cláusulas contratuais", 3, 30, 40, 60),
            ("Protocolar documento", "Enviar petição ou documento ao tribunal", 1, 15, 20, 15),
        ],
    },
    {
        "name": "Profissional de RH",
        "icon": "🤝",
        "category": "negocios",
        "description": "Pessoas, cultura, recrutamento e gestão de talentos.",
        "missions": [
            ("Conduzir entrevista", "Realizar processo seletivo com candidato", 2, 20, 30, 60),
            ("Fazer onboarding", "Integrar novo colaborador à empresa", 2, 25, 30, 60),
            ("Analisar clima organizacional", "Revisar pesquisa ou feedbacks da equipe", 2, 20, 25, 30),
            ("Atualizar registro de colaborador", "Manter dados de funcionários atualizados", 1, 10, 15, 20),
            ("Elaborar plano de desenvolvimento", "Criar PDI para colaborador", 3, 30, 40, 60),
            ("Conduzir reunião 1:1", "Feedback individual com colaborador", 2, 20, 25, 30),
        ],
    },
    # ── TECNOLOGIA ─────────────────────────────────────────────────────
    {
        "name": "Programador(a)",
        "icon": "💻",
        "category": "tecnologia",
        "description": "Desenvolvimento de software, código e sistemas.",
        "missions": [
            ("Revisar Pull Request", "Analisar e comentar código de colega", 2, 20, 30, 30),
            ("Escrever testes", "Criar testes unitários ou de integração", 2, 25, 30, 45),
            ("Resolver bug", "Identificar causa raiz e corrigir problema", 3, 30, 40, 60),
            ("Documentar função ou módulo", "Escrever documentação técnica clara", 1, 15, 20, 30),
            ("Fazer deploy", "Publicar versão em ambiente de produção", 2, 25, 30, 30),
            ("Planejar sprint", "Estimar e priorizar tarefas da semana", 2, 20, 25, 45),
            ("Estudar tecnologia nova", "Explorar biblioteca, framework ou conceito", 2, 20, 25, 60),
        ],
    },
    {
        "name": "Designer",
        "icon": "🎨",
        "category": "tecnologia",
        "description": "Design de produto, UI/UX e comunicação visual.",
        "missions": [
            ("Criar wireframe", "Esboçar fluxo ou tela de novo recurso", 2, 20, 30, 45),
            ("Revisar protótipo", "Testar fluxo e ajustar experiência do usuário", 2, 20, 25, 30),
            ("Pesquisar referências", "Explorar tendências e benchmarks visuais", 1, 15, 20, 30),
            ("Apresentar proposta ao cliente", "Mostrar e discutir conceito de design", 2, 25, 30, 60),
            ("Exportar assets", "Preparar arquivos para desenvolvedores", 1, 15, 20, 20),
            ("Atualizar design system", "Manter biblioteca de componentes atualizada", 2, 20, 25, 40),
        ],
    },
    {
        "name": "Analista de Dados",
        "icon": "📈",
        "category": "tecnologia",
        "description": "Análise, visualização e inteligência de dados.",
        "missions": [
            ("Limpar e tratar dataset", "Remover inconsistências e preparar dados", 2, 25, 30, 60),
            ("Criar dashboard", "Construir ou atualizar painel de métricas", 3, 30, 40, 90),
            ("Analisar tendências", "Identificar padrões nos dados do período", 3, 30, 40, 60),
            ("Apresentar insights", "Compartilhar descobertas com a equipe", 2, 25, 30, 30),
            ("Escrever query SQL", "Criar consulta para extrair dados específicos", 2, 20, 25, 30),
            ("Documentar pipeline", "Registrar fluxo de tratamento de dados", 1, 15, 20, 30),
        ],
    },
    # ── EDUCAÇÃO ───────────────────────────────────────────────────────
    {
        "name": "Professor(a)",
        "icon": "📚",
        "category": "educacao",
        "description": "Ensino, planejamento pedagógico e desenvolvimento de alunos.",
        "missions": [
            ("Preparar aula", "Elaborar plano de aula e materiais didáticos", 2, 20, 30, 45),
            ("Corrigir avaliação", "Corrigir provas ou trabalhos dos alunos", 2, 25, 30, 60),
            ("Dar feedback aos alunos", "Comentar desempenho e orientar melhoras", 2, 20, 25, 30),
            ("Planejar semana pedagógica", "Organizar conteúdos e atividades da semana", 2, 20, 25, 30),
            ("Atualizar diário de classe", "Lançar frequência e notas no sistema", 1, 10, 15, 20),
            ("Reunião com pais", "Discutir desenvolvimento do aluno", 2, 20, 25, 45),
            ("Estudar metodologias ativas", "Pesquisar novas abordagens de ensino", 2, 20, 25, 45),
        ],
    },
    {
        "name": "Pedagogo(a)",
        "icon": "🏫",
        "category": "educacao",
        "description": "Coordenação pedagógica, orientação e desenvolvimento educacional.",
        "missions": [
            ("Elaborar plano pedagógico", "Definir objetivos e estratégias educacionais", 3, 30, 40, 60),
            ("Observar aluno em sala", "Acompanhar comportamento e aprendizagem", 2, 20, 25, 45),
            ("Reunião com pais ou responsáveis", "Orientar família sobre desenvolvimento", 2, 20, 25, 45),
            ("Pesquisar metodologia pedagógica", "Explorar abordagem ou teoria educacional", 2, 20, 25, 45),
            ("Orientar professor", "Dar suporte e feedback a docentes", 2, 20, 25, 30),
            ("Organizar eventos pedagógicos", "Planejar feira, semana temática ou projeto", 2, 25, 30, 60),
        ],
    },
    # ── OUTROS ─────────────────────────────────────────────────────────
    {
        "name": "Nutricionista",
        "icon": "🥗",
        "category": "outros",
        "description": "Alimentação saudável, planos alimentares e saúde nutricional.",
        "missions": [
            ("Elaborar plano alimentar", "Criar dieta personalizada para paciente", 3, 30, 40, 60),
            ("Consulta de retorno", "Avaliar evolução e ajustar plano alimentar", 2, 20, 30, 45),
            ("Calcular cardápio", "Calcular macros e micros de refeições", 2, 25, 30, 45),
            ("Estudar nutrição clínica", "Pesquisar evidência sobre protocolo alimentar", 2, 20, 25, 45),
            ("Atualizar prontuário", "Registrar dados antropométricos do paciente", 1, 10, 15, 15),
            ("Orientar paciente", "Tirar dúvidas sobre alimentação e hábitos", 1, 15, 20, 20),
        ],
    },
    {
        "name": "Arquiteto(a)",
        "icon": "🏛️",
        "category": "outros",
        "description": "Projetos arquitetônicos, obras e espaços.",
        "missions": [
            ("Revisar projeto", "Checar erros e ajustes no projeto técnico", 3, 30, 40, 90),
            ("Visita de obra", "Acompanhar andamento e qualidade da construção", 2, 25, 30, 120),
            ("Elaborar memorial descritivo", "Escrever documento técnico do projeto", 2, 25, 30, 60),
            ("Reunião com cliente", "Apresentar ou discutir projeto com contratante", 2, 20, 30, 60),
            ("Fazer renderização", "Criar visualização 3D de ambiente projetado", 3, 35, 45, 120),
            ("Atualizar pranchas técnicas", "Revisar plantas e cortes do projeto", 2, 25, 30, 60),
        ],
    },
    {
        "name": "Engenheiro(a)",
        "icon": "⚙️",
        "category": "outros",
        "description": "Projetos técnicos, cálculos e gestão de obras ou sistemas.",
        "missions": [
            ("Revisar cálculo técnico", "Checar memória de cálculo ou dimensionamento", 3, 35, 45, 90),
            ("Vistoria de obra ou instalação", "Inspecionar qualidade e conformidade", 2, 25, 30, 120),
            ("Elaborar relatório técnico", "Documentar avaliação ou resultado de ensaio", 2, 25, 30, 60),
            ("Reunião de projeto", "Alinhamento com equipe ou cliente", 2, 20, 25, 60),
            ("Estudar norma técnica", "Revisar ABNT ou regulamentação específica", 2, 20, 25, 45),
            ("Atualizar cronograma", "Revisar prazos e atividades do projeto", 2, 20, 25, 30),
        ],
    },
    {
        "name": "Jornalista",
        "icon": "📰",
        "category": "outros",
        "description": "Apuração, redação e publicação de conteúdo jornalístico.",
        "missions": [
            ("Apurar pauta", "Pesquisar informações e entrevistar fontes", 2, 25, 30, 60),
            ("Escrever matéria", "Redigir texto jornalístico completo", 3, 30, 40, 90),
            ("Revisar texto", "Corrigir gramática, estilo e precisão do texto", 2, 20, 25, 30),
            ("Entrevistar fonte", "Conduzir entrevista para apuração", 2, 25, 30, 45),
            ("Publicar conteúdo", "Formatar e publicar matéria no veículo", 1, 15, 20, 20),
            ("Reunião de pauta", "Discutir temas com a redação", 1, 15, 20, 30),
        ],
    },
    {
        "name": "Vendedor(a)",
        "icon": "🛒",
        "category": "outros",
        "description": "Prospecção, negociação e fechamento de vendas.",
        "missions": [
            ("Prospectar clientes", "Contatar novos potenciais clientes", 2, 20, 25, 30),
            ("Fazer follow-up", "Retornar contato com clientes em negociação", 2, 20, 25, 30),
            ("Apresentar proposta", "Mostrar solução para necessidade do cliente", 2, 25, 30, 45),
            ("Fechar venda", "Concluir negociação e formalizar contrato", 3, 35, 45, 60),
            ("Atualizar CRM", "Registrar atividades e pipeline de vendas", 1, 10, 15, 20),
            ("Estudar produto", "Aprofundar conhecimento sobre o que vende", 1, 15, 20, 30),
        ],
    },
]


def seed_professions(db=None):
    """Seed chamável externamente passando uma sessão, ou cria a própria."""
    own_db = db is None
    if own_db:
        db = SessionLocal()
    try:
        existing = db.query(Profession).count()
        if existing > 0:
            print(f"Profissoes ja existem ({existing} registros). Pulando seed.")
            return

        for prof_data in PROFESSIONS:
            profession = Profession(
                name=prof_data["name"],
                icon=prof_data["icon"],
                category=prof_data["category"],
                description=prof_data["description"],
            )
            db.add(profession)
            db.flush()

            for title, desc, difficulty, coins, xp, minutes in prof_data["missions"]:
                mission = ProfessionMission(
                    profession_id=profession.id,
                    title=title,
                    description=desc,
                    difficulty=difficulty,
                    coin_reward=coins,
                    xp_reward=xp,
                    suggested_minutes=minutes,
                )
                db.add(mission)

        db.commit()
        print(f"OK: {len(PROFESSIONS)} profissoes e suas missoes criadas com sucesso!")
    finally:
        if own_db:
            db.close()


# mantém compatibilidade com execução direta
def seed():
    seed_professions()


if __name__ == "__main__":
    seed()
