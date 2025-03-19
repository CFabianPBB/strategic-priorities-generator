import pandas as pd

def create_excel(priorities):
    data = []
    for p in priorities:
        for definition in p['definitions']:
            data.append({
                'Priority': p['priority'],
                'Description': p['description'],
                'Definition': definition
            })

    df = pd.DataFrame(data)
    file_path = "strategic_priorities.xlsx"
    df.to_excel(file_path, index=False)
    return file_path
