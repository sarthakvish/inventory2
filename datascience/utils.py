import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

def get_image():
    # create bytes buffer to save image or make buffer object
    buffer=BytesIO()
    # create the plot with the use of Bytes io object as its file
    plt.savefig(buffer,format='png')
    # set the curser in the begining to get full image.
    buffer.seek(0) # 0-beg,1-mid,2-end
    # retrive the entire content of file
    image_png=buffer.getvalue()
    graph=base64.b64encode(image_png)
    graph=graph.decode('utf-8')
    # free the memory of buffer
    buffer.close()
    return graph



def get_simple_plot(chart_type, *args, **kwargs):
    plt.switch_backend('AGG') # Study backend matplot lib doc
    fig=plt.figure(figsize=(6,3)) # here will come, x,y, data, df
    x=kwargs.get('x')
    y=kwargs.get('y')
    data=kwargs.get('data')
    data2=kwargs.get('data2')
    if chart_type == 'bar':
        title="Bar Plot"
        plt.title(title)
        plt.bar(x,y)
    elif chart_type == 'line':
        title="Line Plot"
        plt.title(title)
        plt.plot(x,y)
    elif chart_type == 'corr':
        title="Corelation Plot"
        plt.title(title)
        sns.jointplot(x='receive_quantity', y='issue_quantity', kind='reg',height=4, data=data2).set_axis_labels('qunatitiy recieve in company','quantity issue by company')
    else:
        title = "Count Plot"
        plt.title(title)
        sns.countplot('item_name',data=data)
    plt.tight_layout()
    plt.xticks(rotation=45)
    graph=get_image()
    return graph
