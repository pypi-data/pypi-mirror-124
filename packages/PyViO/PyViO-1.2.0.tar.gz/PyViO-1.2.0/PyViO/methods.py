import pandas as pd
import numpy as np
import inspect
allowed = ['show_outliers','donut','display_out']
import warnings
warnings.filterwarnings("ignore")

from PyViO import visuals, methods

def iqr_method(data,parameter): 
    if inspect.stack()[1][3] in allowed:
        outlier = dict()                       #for creating the interactive heatmap's details
        outlier_loc = dict()                   #for creating the count-plot!
        outlier_value = dict()                 #for creating the first df that get returns from here!
        outlier_cat = dict()                   #for creating the interactive heatmap's cat_col details
        outlier_proportion = dict()            #for creating the proportion chart of a feature's outliers

        outlier_count = 0   
        df_size = data.size

        for column in data.describe().columns:
            out_count = 0
            Q1 = np.percentile(data[column], 25, interpolation = 'midpoint')
            Q3 = np.percentile(data[column], 75, interpolation = 'midpoint')
            IQR = Q3 - Q1
            UL = Q3 + (1.5 * IQR)
            LL = Q1 - (1.5 * IQR)

            for row in data[column]:
                if ((row>UL) or (row<LL)):
                    det = []
                    out_count+=1
                    det.append(round(row,2))
                    det.append(data[data[column]==row].index[0])

                    # For positional DF
                    outlier.setdefault(column,[]).append(det)

                    # For interactive DF
                    outlier_value.setdefault(column,[]).append(round(row,2))
                    uid = data[data[column]==row].index[0]
                    cid = " Row Number: "+str(data[data[column]==row].index[0])+" & Column Name: "+str(column)+ " "

                    # For positional DF
                    outlier_cat.setdefault(column,[]).append("Identifiers || " + str(cid) + "|| UL:" + str(UL) + ", LL:" + str(LL) + " ||")

                else:
                    continue
            if (out_count > 0):
                outlier_proportion.setdefault(column,[]).append(out_count)
                outlier_proportion.setdefault(column,[]).append(len(data[column]) - out_count)

            outlier_count+=out_count           

            # For Plotting
            outlier_loc.setdefault(column,[]).append(out_count)

        if (parameter!="doNotProp"):
            (visuals.display_out(data, outlier, outlier_loc, outlier_cat, outlier_value, outlier_proportion, parameter, df_size=df_size, outlier_count=outlier_count))
        else:
            return(outlier_count, df_size)
    else:
        msg = f"Not allowed"
        raise SystemExit(f"Error: {msg}")

def zs_method(data,parameter):
    if inspect.stack()[1][3] in allowed:
        outlier = dict()                       #for creating the interactive heatmap's details
        outlier_loc = dict()                   #for creating the count-plot!
        outlier_value = dict()                 #for creating the first df that get returns from here!
        outlier_cat = dict()                   #for creating the interactive heatmap's cat_col details
        outlier_proportion = dict()            #for creating the proportion chart of a feature's outliers

        s_data = data
        df_size = data.size
        outlier_count = 0
        main_data=data
        cat_cols = [cols for cols in main_data.columns if cols not in main_data.describe().columns]

        import scipy.stats as stats
        from sklearn import preprocessing

        def normality_test(data):
            # Shapiro-Wilk Test
            from scipy.stats import shapiro
            norm_dist = []
            for id,rows in enumerate(data.describe()):
                stat, p = shapiro(list(data[rows]))
                # interpret
                alpha = 0.05
                if p > alpha:
                    norm_dist.append(data.columns[id])
                else:
                    continue
            return norm_dist

        # Normalize Data
        if (len(normality_test(data))==0):
            standard_scaler = preprocessing.StandardScaler()
            x_scaled = pd.DataFrame(standard_scaler.fit_transform(data[data.describe().columns]), columns=data.describe().columns)
            data=x_scaled
        else: 
            data=data        

        # Treat the data based on the z-score evaluation
        z = np.abs(stats.zscore(data[list(data.describe().columns)]))    
        data_z_score = pd.DataFrame(z,columns=data.describe().columns)
        for i in data_z_score.columns:
            data_z_score[i] = data_z_score[i].apply(lambda x:float(round(x,2)) if x<3 else (str(round(x,2))+",outlier"))

        data_z_score = pd.concat([data_z_score,main_data[cat_cols]],axis=1)
        data = data_z_score

        for column in data.describe().columns:
            out_count = 0
            for row in data[column]:
                    if (("," in str(row)) and (str(row).split(",")[1] == "outlier")) :
                        det = []
                        out_count+=1
                        det.append(str(row).split(",")[0])
                        det.append(data[data[column]==row].index[0])

                        # For positional DF
                        outlier.setdefault(column,[]).append(det)

                        # For interactive DF
                        outlier_value.setdefault(column,[]).append(round(float(str(row).split(",")[0]),2))
                        uid = data[data[column]==row].index[0]
                        cid = " Row Number: "+str(data[data[column]==row].index[0])+" & Column Name: "+str(column)

                        # For positional DF
                        outlier_cat.setdefault(column,[]).append("Identifiers || " + str(cid))

                    else:
                        continue
            if (out_count > 0):
                outlier_proportion.setdefault(column,[]).append(out_count)
                outlier_proportion.setdefault(column,[]).append(len(data[column]) - out_count)

            outlier_count+=out_count

        # For Plotting
        outlier_loc.setdefault(column,[]).append(out_count)

        if (parameter!="doNotProp"):
            (visuals.display_out(s_data, outlier, outlier_loc, outlier_cat, outlier_value, outlier_proportion, parameter, df_size=df_size, outlier_count=outlier_count))
        else:
            return(outlier_count, df_size)
    else:
        msg = f"Not allowed"
        raise SystemExit(f"Error: {msg}")
        
def hampel_method(data,parameter):
    if inspect.stack()[1][3] in allowed:
        s_data = data
        outlier = dict()                       #for creating the interactive heatmap's details
        outlier_loc = dict()                   #for creating the count-plot!
        outlier_value = dict()                 #for creating the first df that get returns from here!
        outlier_cat = dict()                   #for creating the interactive heatmap's cat_col details
        outlier_proportion = dict()            #for creating the proportion chart of a feature's outliers

        outlier_count = 0
        df_size = data.size

        for column in data.describe().columns:
            out_count = 0
            medi = data[column].median()
            list_a = abs(data[column]-medi)
            hampel = list_a.median()*4.5

            for row in data[column]:
                if (row >= hampel):
                    det = []
                    out_count+=1
                    det.append(round(row,2))
                    det.append(data[data[column]==row].index[0])

                    # For positional DF
                    outlier.setdefault(column,[]).append(det)

                    # For interactive DF
                    outlier_value.setdefault(column,[]).append(round(row,2))
                    uid = data[data[column]==row].index[0]
                    cid = " Row Number: "+str(data[data[column]==row].index[0])+" & Column Name: "+str(column)

                    # For positional DF
                    outlier_cat.setdefault(column,[]).append("Identifiers || " + str(cid) + " ||")

                else:
                    continue           

            if (out_count > 0):
                outlier_proportion.setdefault(column,[]).append(out_count)
                outlier_proportion.setdefault(column,[]).append(len(data[column]) - out_count)

            # For Plotting
            outlier_loc.setdefault(column,[]).append(out_count)

            outlier_count+=out_count

        if (parameter!="doNotProp"):
            (visuals.display_out(s_data, outlier, outlier_loc, outlier_cat, outlier_value, outlier_proportion, parameter, df_size=df_size, outlier_count=outlier_count))
        else:
            return(outlier_count, df_size)
    else:
        msg = f"Not allowed"
        raise SystemExit(f"Error: {msg}")
