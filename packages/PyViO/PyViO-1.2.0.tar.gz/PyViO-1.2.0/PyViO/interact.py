from PyViO import methods
import warnings
warnings.filterwarnings("ignore")

def show_outliers(data,method,parameter=None):
    """
    A library to visualize the outliers present in data.
    data (mandatory) : The dataframe to be used
    method (mandatory):  Method to use ['iqr','zs','hampel']
    parameter (optional): The name of the column for which the correlation is to be plotted
                          If no value for arguement "parameter" is passed, 
                          the complete correlation matrix will be plotted
    """
    
    parameter="" if (parameter==None) else parameter
    m_data = data

    if (parameter!=""):
        if (parameter in m_data.describe().columns.to_list()):
            True
        else:
            param = parameter                     
            msg = f"{param} is not a valid column name"
            raise SystemExit(f"Error: {msg}")
    else:
        True

    if(method.lower()=='iqr'):
        methods.iqr_method(m_data,parameter)
    elif (method.lower()=='hampel'):
        methods.hampel_method(m_data,parameter)
    elif (method.lower()=='zs'):
        methods.zs_method(m_data,parameter)
    else:
        msg = f"We are not having methods other than [iqr, zs & hampel] currently"
        raise SystemExit(f"Error: {msg}")
