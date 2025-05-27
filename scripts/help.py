def show_help(language="ru"):
    help_content = {
    "ru": {
    "title": "📖 Руководство по интерпретации карт эмоций",
    "sections": [
    {"title": "1. Карта эмоций (t-SNE)", "content": "Визуализирует эмоциональные паттерны в двумерном пространстве.\n- Близкие точки: схожие эмоциональные состояния\n- Цвета: разные категории эмоций\n- Используйте легенду для идентификации"},
    {"title": "2. Ментальная карта (PCA)", "content": "Отображает главные компоненты эмоциональных данных:\n- Ось X: Основной паттерн изменчивости\n- Ось Y: Второстепенный паттерн\n- Метки показывают доминирующую эмоцию отрезка"},
    {"title": "3. Временная диаграмма", "content": "Показывает динамику эмоций во времени:\n- Ширина полос: длительность сегмента (10 сек)\n- Цвет: текущая эмоция\n- Вертикальная ось: последовательность отрезков"},
    {"title": "4. UMAP проекция", "content": "Альтернативный метод визуализации многомерных данных:\n- Сохраняет как глобальную, так и локальную структуру\n- Кластеры: эмоционально близкие группы"},
    {"title": "5. Тепловая карта", "content": "Отображает интенсивность эмоций:\n- Длина полосы: относительная частота\n- Градация цвета: от слабой (светлый) до сильной (темный)\n- Проценты показывают долю каждой эмоции"}
    ],
    "tips": "🔍 Советы:\n- Сравнивайте разные проекции для полной картины\n- Обращайте внимание на кластеры и выбросы\n- Используйте временную диаграмму для анализа изменений"
    },
    "en": {
    "title": "📖 Emotion Maps Interpretation Guide",
    "sections": [
    {"title": "1. Emotion Map (t-SNE)", "content": "Visualizes emotional patterns in 2D space:\n- Close points: similar emotional states\n- Colors: different emotion categories\n- Use legend for identification"},
    {"title": "2. Mental Map (PCA)", "content": "Shows principal components of emotional data:\n- X-axis: Primary variation pattern\n- Y-axis: Secondary variation pattern\n- Labels show dominant segment emotion"},
    {"title": "3. Temporal Chart", "content": "Displays emotion dynamics over time:\n- Band width: segment duration (10 sec)\n- Color: current emotion\n- Vertical axis: sequence of segments"},
    {"title": "4. UMAP Projection", "content": "Alternative multidimensional visualization:\n- Preserves both global and local structure\n- Clusters: emotionally similar groups"},
    {"title": "5. Heatmap", "content": "Shows emotion intensity:\n- Bar length: relative frequency\n- Color gradient: weak (light) to strong (dark)\n- Percentages show emotion share"}
    ],
    "tips": "🔍 Tips:\n- Compare different projections for full picture\n- Note clusters and outliers\n- Use temporal chart to track changes"
    }
    }
    return help_content.get(language, help_content["ru"])