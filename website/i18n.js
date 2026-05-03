const HF_LANGS = {
  es: {
    label: 'Español', dir: 'ltr',
    navHome: 'Inicio', navScanner: 'Escáner', navModules: 'Módulos', navWorkflow: 'Flujo', navGithub: 'GitHub', navSupport: 'Apoyar', navWebsite: 'Sitio oficial',
    heroKicker: 'ANÁLISIS WEB PASIVO DE BAJO RUIDO',
    heroTitle: 'Hallazgos precisos, evidencia clara y superficie mapeada.',
    heroText: 'HexForge Security Lite es un escáner defensivo enfocado en configuración, superficie cliente, parámetros visibles, formularios y evidencia conservadora para revisión manual segura.',
    startScan: 'Iniciar análisis', demoResults: 'Ver demo', openRepo: 'Abrir repositorio', openWebsite: 'HexForgeAI.dev', supportProject: 'Apoyar el proyecto',
    statModules: 'módulos enfocados', statValidation: 'validación local', statExploit: 'acciones de explotación en Lite', statEdition: 'edición comunitaria defensiva',
    sectionChecks: 'Qué revisa', sectionSignal: 'Hecho para señal, no para ruido.',
    checksText: 'Lite revisa headers, cookies, CORS, TLS, redirecciones, archivos de descubrimiento, metadatos, formularios, parámetros, rutas de endpoints y superficie cliente pasiva.',
    cardHeaders: 'Headers y navegador', cardHeadersText: 'CSP, HSTS, Referrer-Policy, Permissions-Policy, X-Content-Type-Options y protección contra iframes.',
    cardSurface: 'Crawler y mapa de superficie', cardSurfaceText: 'Crawl de solo lectura en mismo origen, rutas visibles, rutas tipo API, parámetros y endpoints sin fuzzing.',
    cardEvidence: 'Evidencia y traducciones', cardEvidenceText: 'Cada hallazgo incluye ubicación, evidencia, recomendación, confianza y renderizado multilenguaje.',
    workflowTitle: 'Escanear → Mapear → Validar → Decidir.', workflowText: 'HexForge Lite se mantiene conservador: obtiene el sitio de forma segura, mapea la superficie visible, valida hallazgos y deja la confirmación activa a revisión manual autorizada.',
    flow1: 'Normalizar URL', flow2: 'Obtener de forma segura', flow3: 'Mapear rutas y formularios', flow4: 'Validar y deduplicar', flow5: 'Renderizar reporte traducido',
    liteBoundaryTitle: 'Seguro por diseño.', liteBoundaryText: 'La edición comunitaria es útil sin convertirse en un framework ofensivo.',
    boundary1: 'Chequeos pasivos HTTP/TLS', boundary2: 'Crawler de solo lectura con límites pequeños', boundary3: 'Descubrimiento de parámetros y formularios sin envío', boundary4: 'Sin fuerza bruta ni automatización de exploits',
    supportTitle: 'Apoya el desarrollo de HexForge', supportText: 'Si HexForge Security Lite te ayuda, puedes apoyar el desarrollo o visitar el sitio oficial HexForgeAI.',
    scannerTitle: 'Ejecutar análisis Lite', scannerText: 'Ingresa una URL autorizada o de laboratorio. HexForge Lite no explota, no fuerza y no evade controles.',
    targetLabel: 'URL objetivo', scanButton: 'Analizar objetivo', quickLabs: 'Labs seguros', quickCloudflare: 'Ejemplo fuerte', quickJuice: 'Juice Shop', quickVulnweb: 'VulnWeb',
    guardrailsTitle: 'Límites de Lite', guardrail1: 'Solo revisión pasiva HTTP/TLS.', guardrail2: 'Crawler de solo lectura en mismo origen con límites pequeños.', guardrail3: 'Sin fuzzing, payload spraying, fuerza bruta o bypass.', guardrail4: 'Úsalo solo en objetivos propios, labs o con autorización explícita.',
    mapHint: 'El mapa de endpoints aparece en resultados.', parameterHint: 'Los parámetros visibles se extraen de forma conservadora.', formHint: 'Los formularios se mapean sin enviarlos.',
    resultsTitle: 'Reporte de análisis', targetPrefix: 'Objetivo', riskScore: 'Puntaje de riesgo', findings: 'Hallazgos', high: 'Alto', precision: 'Precisión', passive: 'pasivo', total: 'total', review: 'revisión',
    evidenceRecommendations: 'Evidencia y recomendaciones', runAnother: 'Ejecutar otro análisis', noFindings: 'No hay hallazgos visibles', noFindingsText: 'El análisis no devolvió hallazgos visibles para este objetivo.',
    location: 'Ubicación', evidence: 'Evidencia', recommendation: 'Recomendación', precisionNote: 'Nota de precisión', confidence: 'Confianza',
    surfaceTitle: 'Mapa visual de endpoints', surfaceText: 'Rutas, rutas tipo API, parámetros y formularios extraídos en modo de solo lectura.',
    routesLabel: 'Rutas', apiRoutesLabel: 'Rutas tipo API', paramsLabel: 'Parámetros', formsLabel: 'Formularios', scriptsLabel: 'Scripts', pagesCrawled: 'Páginas leídas', emptySurface: 'No se detectó superficie adicional.', formAction: 'Acción', formMethod: 'Método', fields: 'Campos',
  },
  en: {
    label: 'English', dir: 'ltr',
    navHome: 'Home', navScanner: 'Scanner', navModules: 'Modules', navWorkflow: 'Workflow', navGithub: 'GitHub', navSupport: 'Support', navWebsite: 'Official site',
    heroKicker: 'LOW-NOISE PASSIVE WEB SECURITY ANALYSIS',
    heroTitle: 'Precise findings, clear evidence and mapped surface.',
    heroText: 'HexForge Security Lite is a defensive scanner focused on configuration, client surface, visible parameters, forms, and conservative evidence for safer manual review.',
    startScan: 'Start scan', demoResults: 'View demo', openRepo: 'Open repository', openWebsite: 'HexForgeAI.dev', supportProject: 'Support the project',
    statModules: 'focused modules', statValidation: 'local validation', statExploit: 'exploit actions in Lite', statEdition: 'defensive community edition',
    sectionChecks: 'What it checks', sectionSignal: 'Built for signal, not noise.',
    checksText: 'Lite reviews headers, cookies, CORS, TLS, redirects, discovery files, metadata, forms, parameters, endpoint routes and passive client surface.',
    cardHeaders: 'Headers and browser', cardHeadersText: 'CSP, HSTS, Referrer-Policy, Permissions-Policy, X-Content-Type-Options and iframe protection.',
    cardSurface: 'Crawler and surface map', cardSurfaceText: 'Read-only same-origin crawl, visible routes, API-like paths, query parameters and endpoint mapping without fuzzing.',
    cardEvidence: 'Evidence and translations', cardEvidenceText: 'Every finding includes location, evidence, recommendation, confidence and multi-language rendering.',
    workflowTitle: 'Scan → Map → Validate → Decide.', workflowText: 'HexForge Lite stays conservative: it fetches safely, maps visible surface, validates findings, and leaves active confirmation to authorized manual review.',
    flow1: 'Normalize URL', flow2: 'Fetch safely', flow3: 'Map routes and forms', flow4: 'Validate & deduplicate', flow5: 'Render translated report',
    liteBoundaryTitle: 'Safer by design.', liteBoundaryText: 'The community edition is intentionally useful without becoming an exploit framework.',
    boundary1: 'Passive HTTP/TLS checks', boundary2: 'Read-only crawler with small limits', boundary3: 'Parameter and form discovery without submission', boundary4: 'No brute force or exploit payload automation',
    supportTitle: 'Support HexForge development', supportText: 'If HexForge Security Lite helps you, support development or visit the official HexForgeAI site.',
    scannerTitle: 'Run Lite analysis', scannerText: 'Enter an authorized or lab URL. HexForge Lite does not exploit, brute force or bypass controls.',
    targetLabel: 'Target URL', scanButton: 'Analyze target', quickLabs: 'Safe labs', quickCloudflare: 'Strong example', quickJuice: 'Juice Shop', quickVulnweb: 'VulnWeb',
    guardrailsTitle: 'Lite guardrails', guardrail1: 'Passive HTTP/TLS review only.', guardrail2: 'Read-only same-origin crawler with small limits.', guardrail3: 'No fuzzing, payload spraying, brute force or bypass.', guardrail4: 'Use only on owned, lab, or explicitly authorized targets.',
    mapHint: 'Endpoint map is included in results.', parameterHint: 'Visible parameters are extracted conservatively.', formHint: 'Forms are mapped without submission.',
    resultsTitle: 'Analysis report', targetPrefix: 'Target', riskScore: 'Risk score', findings: 'Findings', high: 'High', precision: 'Precision', passive: 'passive', total: 'total', review: 'review',
    evidenceRecommendations: 'Evidence and recommendations', runAnother: 'Run another scan', noFindings: 'No visible findings', noFindingsText: 'The scan did not return visible findings for this target.',
    location: 'Location', evidence: 'Evidence', recommendation: 'Recommendation', precisionNote: 'Precision note', confidence: 'Confidence',
    surfaceTitle: 'Visual endpoint map', surfaceText: 'Routes, API-like paths, parameters and forms extracted in read-only mode.',
    routesLabel: 'Routes', apiRoutesLabel: 'API-like routes', paramsLabel: 'Parameters', formsLabel: 'Forms', scriptsLabel: 'Scripts', pagesCrawled: 'Pages read', emptySurface: 'No additional surface was detected.', formAction: 'Action', formMethod: 'Method', fields: 'Fields',
  },
  pt: {
    label: 'Português', dir: 'ltr',
    navHome: 'Início', navScanner: 'Scanner', navModules: 'Módulos', navWorkflow: 'Fluxo', navGithub: 'GitHub', navSupport: 'Apoiar', navWebsite: 'Site oficial',
    heroKicker: 'ANÁLISE PASSIVA WEB DE BAIXO RUÍDO', heroTitle: 'Achados precisos, evidência clara e superfície mapeada.', heroText: 'HexForge Security Lite é um scanner defensivo focado em configuração, superfície cliente, parâmetros visíveis, formulários e evidência conservadora.',
    startScan: 'Iniciar análise', demoResults: 'Ver demo', openRepo: 'Abrir repositório', openWebsite: 'HexForgeAI.dev', supportProject: 'Apoiar o projeto',
    statModules: 'módulos focados', statValidation: 'validação local', statExploit: 'ações de exploit no Lite', statEdition: 'edição comunitária defensiva',
    sectionChecks: 'O que verifica', sectionSignal: 'Feito para sinal, não ruído.', checksText: 'Lite revisa headers, cookies, CORS, TLS, redirecionamentos, arquivos de descoberta, metadados, formulários, parâmetros e superfície cliente passiva.',
    cardHeaders: 'Headers e navegador', cardHeadersText: 'CSP, HSTS, Referrer-Policy, Permissions-Policy, X-Content-Type-Options e proteção contra iframe.', cardSurface: 'Crawler e mapa de superfície', cardSurfaceText: 'Crawl somente leitura, rotas visíveis, caminhos tipo API e parâmetros sem fuzzing.', cardEvidence: 'Evidência e traduções', cardEvidenceText: 'Cada achado inclui localização, evidência, recomendação e confiança.',
    workflowTitle: 'Escanear → Mapear → Validar → Decidir.', workflowText: 'HexForge Lite permanece conservador e deixa a confirmação ativa para revisão manual autorizada.', flow1: 'Normalizar URL', flow2: 'Buscar com segurança', flow3: 'Mapear rotas e formulários', flow4: 'Validar e deduplicar', flow5: 'Renderizar relatório traduzido',
    liteBoundaryTitle: 'Mais seguro por design.', liteBoundaryText: 'A edição comunitária é útil sem virar framework ofensivo.', boundary1: 'Checagens passivas HTTP/TLS', boundary2: 'Crawler somente leitura com limites', boundary3: 'Descoberta de parâmetros e formulários sem envio', boundary4: 'Sem força bruta nem automação de exploit',
    supportTitle: 'Apoie o desenvolvimento do HexForge', supportText: 'Se o HexForge Security Lite te ajuda, apoie o desenvolvimento ou visite o site oficial.', scannerTitle: 'Executar análise Lite', scannerText: 'Informe uma URL autorizada ou de laboratório.', targetLabel: 'URL alvo', scanButton: 'Analisar alvo', quickLabs: 'Labs seguros', quickCloudflare: 'Exemplo forte', quickJuice: 'Juice Shop', quickVulnweb: 'VulnWeb',
    guardrailsTitle: 'Limites do Lite', guardrail1: 'Somente revisão passiva HTTP/TLS.', guardrail2: 'Crawler de mesma origem e somente leitura.', guardrail3: 'Sem fuzzing, brute force ou bypass.', guardrail4: 'Use apenas em alvos próprios, labs ou autorizados.', mapHint: 'Mapa de endpoints incluído nos resultados.', parameterHint: 'Parâmetros visíveis são extraídos de forma conservadora.', formHint: 'Formulários são mapeados sem submissão.',
    resultsTitle: 'Relatório de análise', targetPrefix: 'Alvo', riskScore: 'Pontuação de risco', findings: 'Achados', high: 'Alto', precision: 'Precisão', passive: 'passivo', total: 'total', review: 'revisão', evidenceRecommendations: 'Evidência e recomendações', runAnother: 'Executar outra análise', noFindings: 'Nenhum achado visível', noFindingsText: 'A análise não retornou achados visíveis para este alvo.', location: 'Local', evidence: 'Evidência', recommendation: 'Recomendação', precisionNote: 'Nota de precisão', confidence: 'Confiança', surfaceTitle: 'Mapa visual de endpoints', surfaceText: 'Rotas, caminhos tipo API, parâmetros e formulários extraídos em modo somente leitura.', routesLabel: 'Rotas', apiRoutesLabel: 'Rotas tipo API', paramsLabel: 'Parâmetros', formsLabel: 'Formulários', scriptsLabel: 'Scripts', pagesCrawled: 'Páginas lidas', emptySurface: 'Nenhuma superfície adicional foi detectada.', formAction: 'Ação', formMethod: 'Método', fields: 'Campos',
  },
  ja: {
    label: '日本語', dir: 'ltr',
    navHome: 'ホーム', navScanner: 'スキャナー', navModules: 'モジュール', navWorkflow: 'ワークフロー', navGithub: 'GitHub', navSupport: '支援', navWebsite: '公式サイト', heroKicker: '低ノイズの受動的Webセキュリティ分析', heroTitle: '正確な所見、明確な証拠、可視化されたサーフェス。', heroText: 'HexForge Security Lite は設定、クライアント面、可視パラメータ、フォームを保守的に確認する防御的スキャナーです。', startScan: 'スキャン開始', demoResults: 'デモを見る', openRepo: 'リポジトリ', openWebsite: 'HexForgeAI.dev', supportProject: 'プロジェクトを支援', statModules: '重点モジュール', statValidation: 'ローカル検証', statExploit: 'Liteの攻撃動作', statEdition: '防御的コミュニティ版', sectionChecks: '確認内容', sectionSignal: 'ノイズよりシグナル。', checksText: 'Lite はヘッダー、Cookie、CORS、TLS、リダイレクト、メタデータ、フォーム、パラメータ、受動的クライアント面を確認します。', cardHeaders: 'ヘッダーとブラウザ', cardHeadersText: 'CSP、HSTS、Referrer-Policy、Permissions-Policy など。', cardSurface: 'クローラとサーフェスマップ', cardSurfaceText: '同一オリジンを読み取り専用で走査し、ルートやAPI風パスを抽出します。', cardEvidence: '証拠と翻訳', cardEvidenceText: '各所見に位置、証拠、推奨、信頼度を表示します。', workflowTitle: 'スキャン → マップ → 検証 → 判断。', workflowText: 'HexForge Lite は保守的に動作し、能動的な確認は認可された手動レビューに任せます。', flow1: 'URL正規化', flow2: '安全に取得', flow3: 'ルートとフォームを抽出', flow4: '検証と重複排除', flow5: '翻訳レポート表示', liteBoundaryTitle: '安全重視の設計。', liteBoundaryText: 'コミュニティ版は有用でありつつ攻撃フレームワークにはなりません。', boundary1: '受動的HTTP/TLSチェック', boundary2: '小さな読み取り専用クローラ', boundary3: '送信しないパラメータ/フォーム検出', boundary4: '総当たりやexploit自動化なし', supportTitle: 'HexForge の開発を支援', supportText: 'HexForge Security Lite が役立ったら支援または公式サイトをご覧ください。', scannerTitle: 'Lite分析を実行', scannerText: '認可済みまたはラボURLを入力してください。', targetLabel: '対象URL', scanButton: '対象を分析', quickLabs: '安全なラボ', quickCloudflare: '強い例', quickJuice: 'Juice Shop', quickVulnweb: 'VulnWeb', guardrailsTitle: 'Liteのガードレール', guardrail1: '受動的なHTTP/TLS確認のみ。', guardrail2: '同一オリジンの読み取り専用クローラ。', guardrail3: 'fuzzing・総当たり・bypass なし。', guardrail4: '所有・ラボ・明示許可の対象のみ。', mapHint: '結果にエンドポイントマップを表示。', parameterHint: '可視パラメータを保守的に抽出。', formHint: 'フォームは送信せずにマップ化。', resultsTitle: '分析レポート', targetPrefix: '対象', riskScore: 'リスクスコア', findings: '所見', high: '高', precision: '精度', passive: '受動', total: '合計', review: 'レビュー', evidenceRecommendations: '証拠と推奨', runAnother: '別のスキャン', noFindings: '可視所見なし', noFindingsText: 'この対象では可視所見がありませんでした。', location: '場所', evidence: '証拠', recommendation: '推奨', precisionNote: '精度メモ', confidence: '信頼度', surfaceTitle: '視覚的エンドポイントマップ', surfaceText: 'ルート、API風パス、パラメータ、フォームを読み取り専用で抽出。', routesLabel: 'ルート', apiRoutesLabel: 'API風ルート', paramsLabel: 'パラメータ', formsLabel: 'フォーム', scriptsLabel: 'スクリプト', pagesCrawled: '読取ページ数', emptySurface: '追加のサーフェスは検出されませんでした。', formAction: 'アクション', formMethod: 'メソッド', fields: 'フィールド',
  },
  zh: {
    label: '中文', dir: 'ltr',
    navHome: '首页', navScanner: '扫描器', navModules: '模块', navWorkflow: '流程', navGithub: 'GitHub', navSupport: '支持', navWebsite: '官网', heroKicker: '低噪声被动式 Web 安全分析', heroTitle: '精确发现、清晰证据、可视化攻击面。', heroText: 'HexForge Security Lite 是一个防御型扫描器，关注配置、客户端表面、可见参数、表单以及保守证据。', startScan: '开始扫描', demoResults: '查看演示', openRepo: '打开仓库', openWebsite: 'HexForgeAI.dev', supportProject: '支持项目', statModules: '聚焦模块', statValidation: '本地验证', statExploit: 'Lite 中的利用动作', statEdition: '防御社区版', sectionChecks: '检查内容', sectionSignal: '为信号而生，而非噪音。', checksText: 'Lite 检查标头、Cookie、CORS、TLS、重定向、发现文件、元数据、表单、参数和被动客户端表面。', cardHeaders: '标头与浏览器', cardHeadersText: 'CSP、HSTS、Referrer-Policy、Permissions-Policy 等。', cardSurface: '爬虫与表面地图', cardSurfaceText: '只读同源爬取，可见路由、API 风格路径和参数映射，无 fuzzing。', cardEvidence: '证据与翻译', cardEvidenceText: '每个发现都包含位置、证据、建议和置信度。', workflowTitle: '扫描 → 映射 → 验证 → 决定。', workflowText: 'HexForge Lite 保持保守，将主动确认留给授权的人工审查。', flow1: '规范化 URL', flow2: '安全获取', flow3: '映射路由与表单', flow4: '验证并去重', flow5: '输出翻译报告', liteBoundaryTitle: '设计更安全。', liteBoundaryText: '社区版有用，但不会成为攻击框架。', boundary1: '被动 HTTP/TLS 检查', boundary2: '小型只读爬虫', boundary3: '不提交的参数与表单发现', boundary4: '无暴力破解与利用自动化', supportTitle: '支持 HexForge 开发', supportText: '如果 HexForge Security Lite 对你有帮助，请支持开发或访问官网。', scannerTitle: '运行 Lite 分析', scannerText: '输入授权目标或实验室 URL。', targetLabel: '目标 URL', scanButton: '分析目标', quickLabs: '安全实验室', quickCloudflare: '强示例', quickJuice: 'Juice Shop', quickVulnweb: 'VulnWeb', guardrailsTitle: 'Lite 护栏', guardrail1: '仅被动 HTTP/TLS 审查。', guardrail2: '小型同源只读爬虫。', guardrail3: '无 fuzzing、暴力破解或绕过。', guardrail4: '仅用于自有、实验室或明确授权目标。', mapHint: '结果中包含端点地图。', parameterHint: '保守提取可见参数。', formHint: '表单在不提交的情况下被映射。', resultsTitle: '分析报告', targetPrefix: '目标', riskScore: '风险分数', findings: '发现', high: '高', precision: '精度', passive: '被动', total: '总计', review: '复核', evidenceRecommendations: '证据与建议', runAnother: '再次扫描', noFindings: '没有可见发现', noFindingsText: '此目标未返回可见发现。', location: '位置', evidence: '证据', recommendation: '建议', precisionNote: '精度说明', confidence: '置信度', surfaceTitle: '可视化端点地图', surfaceText: '只读模式提取路由、API 风格路径、参数和表单。', routesLabel: '路由', apiRoutesLabel: 'API 风格路由', paramsLabel: '参数', formsLabel: '表单', scriptsLabel: '脚本', pagesCrawled: '已读取页面', emptySurface: '未检测到更多表面。', formAction: '动作', formMethod: '方法', fields: '字段',
  },
  ar: {
    label: 'العربية', dir: 'rtl',
    navHome: 'الرئيسية', navScanner: 'الماسح', navModules: 'الوحدات', navWorkflow: 'التدفق', navGithub: 'GitHub', navSupport: 'دعم', navWebsite: 'الموقع الرسمي', heroKicker: 'تحليل أمني ويب سلبي منخفض الضجيج', heroTitle: 'نتائج دقيقة وأدلة واضحة وسطح مرئي.', heroText: 'HexForge Security Lite ماسح دفاعي يركز على الإعدادات وسطح العميل والمعلمات الظاهرة والنماذج والأدلة المحافظة.', startScan: 'ابدأ الفحص', demoResults: 'عرض demo', openRepo: 'فتح المستودع', openWebsite: 'HexForgeAI.dev', supportProject: 'ادعم المشروع', statModules: 'وحدات مركزة', statValidation: 'تحقق محلي', statExploit: 'إجراءات exploit في Lite', statEdition: 'إصدار مجتمعي دفاعي', sectionChecks: 'ما الذي يفحصه', sectionSignal: 'مصمم للإشارة لا للضجيج.', checksText: 'يفحص Lite الرؤوس وملفات الارتباط و CORS و TLS وإعادة التوجيه والبيانات الوصفية والنماذج والمعلمات وسطح العميل السلبي.', cardHeaders: 'الرؤوس والمتصفح', cardHeadersText: 'CSP و HSTS و Referrer-Policy و Permissions-Policy وغيرها.', cardSurface: 'الزاحف وخريطة السطح', cardSurfaceText: 'زحف للقراءة فقط داخل نفس الأصل مع استخراج المسارات والمعلمات بدون fuzzing.', cardEvidence: 'الأدلة والترجمات', cardEvidenceText: 'كل نتيجة تتضمن الموقع والدليل والتوصية والثقة.', workflowTitle: 'افحص → ارسم الخريطة → تحقق → قرر.', workflowText: 'يبقى HexForge Lite محافظا ويترك التأكيد النشط للمراجعة اليدوية المصرح بها.', flow1: 'تطبيع الرابط', flow2: 'جلب آمن', flow3: 'رسم المسارات والنماذج', flow4: 'التحقق وإزالة التكرار', flow5: 'عرض تقرير مترجم', liteBoundaryTitle: 'أكثر أمانا بالتصميم.', liteBoundaryText: 'الإصدار المجتمعي مفيد بدون أن يصبح إطارا هجوميا.', boundary1: 'فحوصات HTTP/TLS سلبية', boundary2: 'زاحف قراءة فقط بحدود صغيرة', boundary3: 'اكتشاف المعلمات والنماذج بدون إرسال', boundary4: 'لا brute force ولا أتمتة exploit', supportTitle: 'ادعم تطوير HexForge', supportText: 'إذا ساعدك HexForge Security Lite فيمكنك دعم التطوير أو زيارة الموقع الرسمي.', scannerTitle: 'شغل تحليل Lite', scannerText: 'أدخل رابطا مصرحا أو من بيئة مختبر.', targetLabel: 'رابط الهدف', scanButton: 'حلل الهدف', quickLabs: 'مختبرات آمنة', quickCloudflare: 'مثال قوي', quickJuice: 'Juice Shop', quickVulnweb: 'VulnWeb', guardrailsTitle: 'قيود Lite', guardrail1: 'مراجعة HTTP/TLS سلبية فقط.', guardrail2: 'زاحف من نفس الأصل للقراءة فقط.', guardrail3: 'بدون fuzzing أو brute force أو bypass.', guardrail4: 'استخدمه فقط على أنظمة تملكها أو مختبرات أو أهداف مصرح بها.', mapHint: 'خريطة endpoints موجودة في النتائج.', parameterHint: 'يتم استخراج المعلمات الظاهرة بشكل محافظ.', formHint: 'يتم رسم النماذج بدون إرسال.', resultsTitle: 'تقرير التحليل', targetPrefix: 'الهدف', riskScore: 'درجة المخاطر', findings: 'النتائج', high: 'مرتفع', precision: 'الدقة', passive: 'سلبي', total: 'الإجمالي', review: 'مراجعة', evidenceRecommendations: 'الدليل والتوصيات', runAnother: 'شغل فحصا آخر', noFindings: 'لا توجد نتائج ظاهرة', noFindingsText: 'لم يُرجع الفحص نتائج ظاهرة لهذا الهدف.', location: 'الموقع', evidence: 'الدليل', recommendation: 'التوصية', precisionNote: 'ملاحظة الدقة', confidence: 'الثقة', surfaceTitle: 'خريطة مرئية للنقاط النهائية', surfaceText: 'استخراج المسارات والمسارات الشبيهة بـ API والمعلمات والنماذج في وضع القراءة فقط.', routesLabel: 'المسارات', apiRoutesLabel: 'مسارات شبيهة بـ API', paramsLabel: 'المعلمات', formsLabel: 'النماذج', scriptsLabel: 'السكربتات', pagesCrawled: 'الصفحات المقروءة', emptySurface: 'لم يتم اكتشاف سطح إضافي.', formAction: 'الإجراء', formMethod: 'الطريقة', fields: 'الحقول',
  },
  hi: {
    label: 'हिन्दी', dir: 'ltr',
    navHome: 'होम', navScanner: 'स्कैनर', navModules: 'मॉड्यूल', navWorkflow: 'वर्कफ़्लो', navGithub: 'GitHub', navSupport: 'समर्थन', navWebsite: 'आधिकारिक साइट', heroKicker: 'लो-नॉइज़ पैसिव वेब सिक्योरिटी एनालिसिस', heroTitle: 'सटीक findings, साफ evidence, mapped surface.', heroText: 'HexForge Security Lite एक defensive scanner है जो configuration, client surface, visible parameters, forms और conservative evidence पर फोकस करता है।', startScan: 'स्कैन शुरू करें', demoResults: 'डेमो देखें', openRepo: 'रिपॉजिटरी खोलें', openWebsite: 'HexForgeAI.dev', supportProject: 'प्रोजेक्ट को सपोर्ट करें', statModules: 'focused modules', statValidation: 'local validation', statExploit: 'Lite में exploit actions', statEdition: 'defensive community edition', sectionChecks: 'यह क्या जांचता है', sectionSignal: 'Signal के लिए बना है, noise के लिए नहीं।', checksText: 'Lite headers, cookies, CORS, TLS, redirects, metadata, forms, parameters और passive client surface review करता है।', cardHeaders: 'Headers और browser', cardHeadersText: 'CSP, HSTS, Referrer-Policy, Permissions-Policy आदि।', cardSurface: 'Crawler और surface map', cardSurfaceText: 'Read-only same-origin crawl, routes, API-like paths और parameters बिना fuzzing के।', cardEvidence: 'Evidence और translations', cardEvidenceText: 'हर finding में location, evidence, recommendation और confidence होता है।', workflowTitle: 'Scan → Map → Validate → Decide.', workflowText: 'HexForge Lite conservative रहता है और active confirmation को authorized manual review के लिए छोड़ता है।', flow1: 'URL normalize करें', flow2: 'Safely fetch करें', flow3: 'Routes और forms map करें', flow4: 'Validate और deduplicate करें', flow5: 'Translated report दिखाएँ', liteBoundaryTitle: 'Design से safer.', liteBoundaryText: 'Community edition useful है लेकिन offensive framework नहीं बनता।', boundary1: 'Passive HTTP/TLS checks', boundary2: 'Read-only crawler with small limits', boundary3: 'Parameter और form discovery बिना submission', boundary4: 'No brute force या exploit automation', supportTitle: 'HexForge development को support करें', supportText: 'अगर HexForge Security Lite मदद करता है, तो development support करें या official site देखें।', scannerTitle: 'Lite analysis चलाएँ', scannerText: 'Authorized या lab URL डालें।', targetLabel: 'Target URL', scanButton: 'Target analyze करें', quickLabs: 'Safe labs', quickCloudflare: 'Strong example', quickJuice: 'Juice Shop', quickVulnweb: 'VulnWeb', guardrailsTitle: 'Lite guardrails', guardrail1: 'केवल passive HTTP/TLS review.', guardrail2: 'Read-only same-origin crawler with small limits.', guardrail3: 'No fuzzing, brute force या bypass.', guardrail4: 'केवल owned, lab या explicitly authorized targets पर use करें.', mapHint: 'Results में endpoint map शामिल है।', parameterHint: 'Visible parameters conservative तरीके से निकाले जाते हैं।', formHint: 'Forms बिना submission के map किए जाते हैं।', resultsTitle: 'Analysis report', targetPrefix: 'Target', riskScore: 'Risk score', findings: 'Findings', high: 'High', precision: 'Precision', passive: 'passive', total: 'total', review: 'review', evidenceRecommendations: 'Evidence और recommendations', runAnother: 'दूसरा scan चलाएँ', noFindings: 'कोई visible finding नहीं', noFindingsText: 'इस target के लिए कोई visible finding नहीं मिली।', location: 'Location', evidence: 'Evidence', recommendation: 'Recommendation', precisionNote: 'Precision note', confidence: 'Confidence', surfaceTitle: 'Visual endpoint map', surfaceText: 'Routes, API-like paths, parameters और forms read-only mode में extract किए गए।', routesLabel: 'Routes', apiRoutesLabel: 'API-like routes', paramsLabel: 'Parameters', formsLabel: 'Forms', scriptsLabel: 'Scripts', pagesCrawled: 'Pages read', emptySurface: 'कोई additional surface detect नहीं हुई।', formAction: 'Action', formMethod: 'Method', fields: 'Fields',
  }
};

const FINDING_TRANSLATIONS = {
  es: {
    'HF-LITE-001': ['Faltan headers de endurecimiento del navegador', 'No se observaron uno o más headers defensivos del navegador en la respuesta.', 'Agrega headers de seguridad conservadores y ajústalos según el comportamiento de la aplicación.'],
    'HF-LITE-002': ['El header Server expone tecnología', 'La respuesta expone detalles de implementación en el header Server.', 'Reduce la divulgación innecesaria en el header Server.'],
    'HF-LITE-004': ['No se observó protección contra iframes', 'No se encontró X-Frame-Options ni CSP frame-ancestors en la respuesta inicial.', 'Configura X-Frame-Options o CSP frame-ancestors en páginas sensibles.'],
    'HF-LITE-005': ['Se observó política CORS wildcard', 'La respuesta permite cualquier origen. Esto no es crítico automáticamente sin datos sensibles o credenciales.', 'Evita CORS wildcard en recursos sensibles o autenticados.'],
    'HF-LITE-025': ['Formulario sin método HTTP explícito', 'Una etiqueta form no declara el atributo method.', 'Declara métodos GET o POST explícitos para evitar comportamiento ambiguo.'],
    'HF-LITE-026': ['Campo de contraseña servido por HTTP', 'La página contiene un campo de contraseña pero el objetivo no usa HTTPS.', 'Sirve los puntos de ingreso de credenciales exclusivamente por HTTPS.'],
    'HF-LITE-027': ['/robots.txt es accesible públicamente', 'El archivo de descubrimiento /robots.txt está disponible públicamente.', 'Revisa si expone rutas internas innecesarias.'],
    'HF-LITE-028': ['/sitemap.xml es accesible públicamente', 'El archivo de descubrimiento /sitemap.xml está disponible públicamente.', 'Revisa si expone rutas internas innecesarias.'],
    'HF-LITE-029': ['TLS y certificado revisados', 'Se capturó un resumen de protocolo TLS y certificado del objetivo.', 'Supervisa el vencimiento del certificado y retira soporte legado.'],
    'HF-LITE-030': ['Falta el header HSTS en un objetivo HTTPS', 'El objetivo usa HTTPS pero no envía Strict-Transport-Security.', 'Agrega HSTS después de confirmar que el sitio está listo para HTTPS forzado.'],
    'HF-LITE-031': ['Se detectó superficie de aplicación cliente', 'La página parece cargar una aplicación cliente o bundles JavaScript que pueden contener rutas para revisión manual.', 'Usa la superficie extraída como mapa de revisión manual; la presencia de bundles no es una vulnerabilidad.'],
    'HF-LITE-032': ['Rutas tipo API referenciadas por el cliente', 'La respuesta cliente o los scripts del mismo origen referencian rutas que parecen API.', 'Verifica manualmente si cada endpoint está en alcance, autenticado correctamente y sin exposición indebida de datos.'],
    'HF-LITE-033': ['Rutas del mismo origen mapeadas para revisión manual', 'La página expone enlaces o acciones del mismo origen que pueden guiar una revisión manual controlada.', 'Usa este mapa solo en activos permitidos por el programa o tu laboratorio.'],
    'HF-LITE-034': ['Parámetros de consulta y formulario descubiertos', 'Las URLs visibles, formularios o referencias cliente exponen nombres de parámetros que pueden guiar una revisión manual segura.', 'Revisa los nombres de parámetros con cuidado. Descubrir parámetros por sí solo no es una vulnerabilidad.'],
    'HF-LITE-036': ['Superficie de formularios mapeada para revisión manual', 'La página expone formularios HTML y nombres de campos que pueden guiar una revisión manual segura. Esto es informativo y no una vulnerabilidad por sí mismo.', 'Revisa acciones, métodos y nombres de campos sin enviar datos automáticamente.'],
    'HF-LITE-037': ['Archivo security.txt observado', 'Un archivo security.txt está accesible públicamente. Esto ayuda a investigadores a encontrar el canal correcto de reporte y es informativo por sí solo.', 'Mantén security.txt preciso, incluye un Contact válido y conserva expiración o enlaces de política según tu proceso de divulgación.'],
    'HF-LITE-038': ['Métodos HTTP observados con OPTIONS seguro', 'El objetivo respondió a una solicitud OPTIONS de bajo impacto y expuso métodos HTTP permitidos. Esto mapea superficie y no es una vulnerabilidad por sí solo.', 'Revisa los métodos expuestos y confirma que los métodos de cambio de estado estén restringidos a flujos autorizados.'],
    'HF-LITE-039': ['Métodos HTTP sensibles anunciados', 'La respuesta OPTIONS anuncia métodos que merecen revisión manual. Esto no prueba que existan cambios de estado sin autenticación.', 'Verifica manualmente autorización y comportamiento del servidor para esos métodos dentro del alcance permitido.'],
    'HF-LITE-040': ['Formulario POST sin marcador anti-CSRF visible', 'Se observó un formulario POST sin un nombre de campo visible comúnmente usado para tokens anti-CSRF. Es solo una señal de revisión.', 'Verifica manualmente si el flujo tiene protección CSRF antes de reportar. No asumas vulnerabilidad solo por el HTML.'],
    'HF-PLUGIN-001': ['Metadata generator observada por plugin Lite', 'Un plugin Lite observó metadata pública de generador en el HTML. Es informativo y no es una vulnerabilidad por sí solo.', 'Revisa si esa metadata pública es intencional. Elimínala o generalízala si expone detalles innecesarios.'],
  },
  pt: {
    'HF-LITE-001': ['Headers de proteção do navegador ausentes', 'Um ou mais headers defensivos do navegador não foram observados.', 'Adicione headers de segurança conservadores e ajuste conforme o comportamento da aplicação.'],
    'HF-LITE-005': ['Política CORS wildcard observada', 'A resposta aceita qualquer origem. Isso não é crítico automaticamente sem dados sensíveis ou credenciais.', 'Evite CORS wildcard em recursos sensíveis ou autenticados.'],
    'HF-LITE-025': ['Formulário sem método HTTP explícito', 'Uma tag form não declara o atributo method.', 'Declare métodos GET ou POST explícitos para evitar comportamento ambíguo.'],
    'HF-LITE-026': ['Campo de senha servido por HTTP', 'A página contém um campo de senha mas o alvo não usa HTTPS.', 'Sirva pontos de entrada de credenciais apenas por HTTPS.'],
    'HF-LITE-030': ['Header HSTS ausente no alvo HTTPS', 'O alvo usa HTTPS mas não envia Strict-Transport-Security.', 'Adicione HSTS após confirmar que o site está pronto para HTTPS forçado.'],
    'HF-LITE-031': ['Superfície de aplicação cliente detectada', 'A página parece carregar uma aplicação cliente ou bundles JavaScript.', 'Use a superfície extraída como mapa de revisão manual; isso não é vulnerabilidade por si só.'],
    'HF-LITE-032': ['Rotas parecidas com API referenciadas pelo cliente', 'A resposta do cliente ou scripts de mesma origem referenciam caminhos parecidos com API.', 'Verifique manualmente cada endpoint.'],
    'HF-LITE-033': ['Rotas de mesma origem mapeadas para revisão manual', 'A página expõe links ou ações de mesma origem úteis para revisão manual.', 'Use este mapa apenas em ativos autorizados.'],
    'HF-LITE-034': ['Parâmetros de consulta e formulário descobertos', 'URLs visíveis, formulários ou referências cliente expõem nomes de parâmetros.', 'Reveja os nomes com cuidado; isso por si só não é vulnerabilidade.'],
    'HF-LITE-036': ['Superfície de formulários mapeada para revisão manual', 'A página expõe formulários HTML e nomes de campos para revisão manual.', 'Revise ações, métodos e nomes de campos sem enviar dados.'],
  },
  ja: {
    'HF-LITE-001': ['ブラウザ強化ヘッダーが不足', '防御的なブラウザヘッダーが確認できませんでした。', '保守的なセキュリティヘッダーを追加してください。'],
    'HF-LITE-005': ['ワイルドカードCORSポリシーを確認', 'レスポンスは任意のオリジンを許可しています。', '機密または認証済みリソースではワイルドカードCORSを避けてください。'],
    'HF-LITE-025': ['フォームに明示的HTTPメソッドがありません', 'form タグに method 属性がありません。', 'GET または POST を明示してください。'],
    'HF-LITE-026': ['パスワード入力がHTTPで提供', 'ページにパスワード入力がありますが HTTPS を使用していません。', '資格情報入力ページは HTTPS のみで提供してください。'],
    'HF-LITE-030': ['HTTPS対象でHSTSヘッダーが不足', '対象は HTTPS を使っていますが Strict-Transport-Security を送信していません。', 'HTTPS 強制の準備後に HSTS を追加してください。'],
    'HF-LITE-031': ['クライアント側アプリ面を検出', 'ページはクライアントアプリや JavaScript バンドルを読み込んでいるようです。', '抽出した面を手動レビュー用マップとして使ってください。'],
    'HF-LITE-032': ['クライアントがAPI風ルートを参照', 'レスポンスまたは同一オリジンスクリプトが API に見えるパスを参照しています。', '各エンドポイントを手動確認してください。'],
    'HF-LITE-033': ['同一オリジンルートをマップ化', 'ページは手動レビューに役立つ同一オリジンのリンクやアクションを公開しています。', '認可された対象でのみ使用してください。'],
    'HF-LITE-034': ['クエリ/フォームパラメータを検出', '可視URL、フォーム、クライアント参照からパラメータ名を抽出しました。', 'パラメータ名の発見自体は脆弱性ではありません。'],
    'HF-LITE-036': ['フォーム面を手動レビュー向けにマップ化', 'ページは手動レビューに役立つフォームと入力名を公開しています。', 'データ送信なしで action・method・field 名を確認してください。'],
  },
  zh: {
    'HF-LITE-001': ['缺少浏览器加固标头', '响应中未观察到一个或多个防御性浏览器标头。', '添加保守的安全标头并按应用行为调整。'],
    'HF-LITE-005': ['观察到通配符 CORS 策略', '响应允许任意来源。', '避免在敏感或认证资源上使用通配符 CORS。'],
    'HF-LITE-025': ['表单缺少显式 HTTP 方法', '某个 form 标签没有声明 method 属性。', '显式声明 GET 或 POST。'],
    'HF-LITE-026': ['密码字段通过 HTTP 提供', '页面包含密码输入框，但目标未使用 HTTPS。', '凭据输入页面应只通过 HTTPS 提供。'],
    'HF-LITE-030': ['HTTPS 目标缺少 HSTS 标头', '目标使用 HTTPS 但未发送 Strict-Transport-Security。', '确认站点可强制 HTTPS 后再添加 HSTS。'],
    'HF-LITE-031': ['检测到客户端应用表面', '页面似乎加载客户端应用或 JavaScript 包。', '将提取到的内容作为人工审查地图使用。'],
    'HF-LITE-032': ['客户端引用了类似 API 的路由', '客户端响应或同源脚本引用了类似 API 的路径。', '手动验证每个端点。'],
    'HF-LITE-033': ['已映射同源路由用于人工审查', '页面暴露了可帮助人工审查的同源链接或动作。', '仅在授权资产上使用此地图。'],
    'HF-LITE-034': ['发现查询与表单参数', '可见 URL、表单或客户端引用暴露了参数名。', '参数发现本身不代表漏洞。'],
    'HF-LITE-036': ['已映射表单表面用于人工审查', '页面暴露 HTML 表单和字段名，可用于人工审查。', '无需自动提交数据即可审查 action、method 和字段名。'],
  },
  ar: {
    'HF-LITE-001': ['رؤوس تقوية المتصفح مفقودة', 'لم تُلاحظ بعض رؤوس المتصفح الدفاعية في الاستجابة.', 'أضف رؤوس أمان محافظة واضبطها حسب الحاجة.'],
    'HF-LITE-005': ['تمت ملاحظة سياسة CORS wildcard', 'تسمح الاستجابة بأي أصل.', 'تجنب CORS wildcard على الموارد الحساسة أو المصادق عليها.'],
    'HF-LITE-025': ['نموذج بدون طريقة HTTP صريحة', 'إحدى وسوم form لا تعلن الخاصية method.', 'صرح بطريقة GET أو POST بشكل واضح.'],
    'HF-LITE-026': ['حقل كلمة مرور مقدم عبر HTTP', 'تحتوي الصفحة على حقل كلمة مرور لكن الهدف لا يستخدم HTTPS.', 'اجعل صفحات إدخال الاعتماديات تعمل عبر HTTPS فقط.'],
    'HF-LITE-030': ['رأس HSTS مفقود على هدف HTTPS', 'الهدف يستخدم HTTPS لكنه لا يرسل Strict-Transport-Security.', 'أضف HSTS بعد التأكد من جاهزية الموقع لفرض HTTPS.'],
    'HF-LITE-031': ['تم اكتشاف سطح تطبيق عميل', 'يبدو أن الصفحة تحمل تطبيقا عميلا أو حزم JavaScript.', 'استخدم السطح المستخرج كخريطة للمراجعة اليدوية.'],
    'HF-LITE-032': ['مسارات تشبه API مشار إليها من العميل', 'الاستجابة أو سكربتات نفس المصدر تشير إلى مسارات تبدو كـ API.', 'تحقق يدويا من كل endpoint.'],
    'HF-LITE-033': ['تم رسم مسارات نفس الأصل للمراجعة اليدوية', 'تعرض الصفحة روابط أو إجراءات من نفس الأصل يمكن أن تفيد في المراجعة اليدوية.', 'استخدم هذه الخريطة فقط على الأصول المصرح بها.'],
    'HF-LITE-034': ['تم اكتشاف معلمات الاستعلام والنماذج', 'تكشف الروابط الظاهرة أو النماذج أو مراجع العميل أسماء معلمات.', 'اكتشاف المعلمات وحده ليس ثغرة.'],
    'HF-LITE-036': ['تم رسم سطح النماذج للمراجعة اليدوية', 'تعرض الصفحة نماذج HTML وأسماء حقول مفيدة للمراجعة اليدوية.', 'راجع action و method وأسماء الحقول دون إرسال بيانات.'],
  },
  hi: {
    'HF-LITE-001': ['Browser hardening headers गायब', 'Response में एक या अधिक defensive browser headers नहीं दिखे।', 'Conservative security headers जोड़ें।'],
    'HF-LITE-005': ['Wildcard CORS policy दिखी', 'Response किसी भी origin को allow करता है।', 'Sensitive या authenticated resources पर wildcard CORS avoid करें।'],
    'HF-LITE-025': ['Form में explicit HTTP method नहीं है', 'एक form tag में method attribute नहीं है।', 'GET या POST method explicitly declare करें।'],
    'HF-LITE-026': ['Password field HTTP पर serve हो रही है', 'Page में password input है लेकिन target HTTPS use नहीं करता।', 'Credential entry points को केवल HTTPS पर serve करें।'],
    'HF-LITE-030': ['HTTPS target पर HSTS header गायब', 'Target HTTPS use करता है लेकिन Strict-Transport-Security नहीं भेजता।', 'Site ready होने के बाद HSTS add करें।'],
    'HF-LITE-031': ['Client-side application surface detected', 'Page client-side app या JavaScript bundles load करती लगती है।', 'Extracted surface को manual review map की तरह use करें।'],
    'HF-LITE-032': ['Client द्वारा API-like routes referenced', 'Client response या same-origin scripts API जैसे paths reference करते हैं।', 'हर endpoint को manually verify करें।'],
    'HF-LITE-033': ['Same-origin routes manual review के लिए mapped', 'Page same-origin links या actions expose करती है जो controlled manual review में मदद करते हैं।', 'इसे केवल authorized assets पर use करें।'],
    'HF-LITE-034': ['Query और form parameters discovered', 'Visible URLs, forms या client references parameter names expose करते हैं।', 'Parameter discovery अपने आप vulnerability नहीं है।'],
    'HF-LITE-036': ['Forms surface manual review के लिए mapped', 'Page HTML forms और field names expose करती है।', 'बिना data submit किए action, method और field names review करें।'],
  }
};

function getLang() {
  const urlLang = new URLSearchParams(location.search).get('lang');
  const stored = localStorage.getItem('hf_lang');
  const candidate = urlLang || stored || 'en';
  return HF_LANGS[candidate] ? candidate : 'en';
}

function setLang(lang) {
  const chosen = HF_LANGS[lang] ? lang : 'en';
  localStorage.setItem('hf_lang', chosen);
  const url = new URL(location.href);
  url.searchParams.set('lang', chosen);
  location.href = url.toString();
}

function applyI18n() {
  const lang = getLang();
  const dict = HF_LANGS[lang] || HF_LANGS.en;
  document.documentElement.lang = lang;
  document.documentElement.dir = dict.dir || 'ltr';
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) el.textContent = dict[key];
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (dict[key]) el.setAttribute('placeholder', dict[key]);
  });
  document.querySelectorAll('[data-lang-select]').forEach((select) => {
    select.value = lang;
  });
  document.querySelectorAll('[data-lang-link]').forEach((link) => {
    const href = new URL(link.getAttribute('href'), location.origin);
    href.searchParams.set('lang', lang);
    link.setAttribute('href', href.pathname + href.search + href.hash);
  });
}

document.addEventListener('DOMContentLoaded', applyI18n);
