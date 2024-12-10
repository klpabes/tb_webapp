import matplotlib.pyplot as plt
import matplotlib
import base64
from io import BytesIO

def get_graph(df_final, year):
    matplotlib.use('agg')
    plt.plot(df_final['MONTH'], df_final['ACTUAL'], label='actual', linewidth = '3')
    # plt.plot(train.index, train, label='Train')
    plt.plot(df_final['MONTH'], df_final['PREDICTED'], label='predicted')
    # plt.plot(predictions.index, predictions, color='green', label='Predicted Cases')
    plt.title(f'Tuberculosis Cases Prediction on {year}')
    plt.xlabel('Month')
    plt.ylabel('Cases')
    plt.xticks(rotation=30, fontsize=8)
    plt.legend()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    plt.close()
    return graphic