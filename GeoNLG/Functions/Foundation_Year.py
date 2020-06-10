import geopandas as gpd

def Foundation_Year(input_layer_path,founding_Field_Name,fid):
    """
    Essence
    -------
    Function returns string of foundation decade for selected building from buildings layer

    Inputes
    -------

    :param input_layer_path: Path of buildings layer (points layer) as .gdb file
    :type String

    :param founding_Field_Name: Founding feature name in Buildings layer
    :type String

    :param fid: Fid of selected building from Buildings layer
    :type Integer

    Returns
    --------

    :return: Foundation decade for selected building
    :type String
    """

    table = gpd.read_file(input_layer_path, encoding='utf-8',driver="OpenFileGDB", errors='ignore',layer=0)


    for index, row in table.iterrows():
        # checking if Height field's values are number
        try:
            int(table.loc[index, founding_Field_Name])
        except(Exception):
            print("Invalid Height Field, Height should be number values, not String")
            exit(0)

        if index == fid:
            try:
                if (int(table.loc[index, founding_Field_Name])> 1940) and (int(table.loc[index, founding_Field_Name])< 1949):
                    return("שנות הארבעים")
                elif (int(table.loc[index, founding_Field_Name])> 1950) and (int(table.loc[index, founding_Field_Name])< 1959):
                    return("שנות החמישים")
                elif (int(table.loc[index, founding_Field_Name]) > 1960) and ( int(table.loc[index, founding_Field_Name]) < 1969):
                    return ("שנות השישים")
                elif (int(table.loc[index, founding_Field_Name]) > 1970) and ( int(table.loc[index, founding_Field_Name]) < 1979):
                    return ("שנות השבעים")
                elif (int(table.loc[index, founding_Field_Name]) > 1980) and ( int(table.loc[index, founding_Field_Name]) < 1989):
                    return ("שנות השמונים")
                elif (int(table.loc[index, founding_Field_Name]) > 1990) and ( int(table.loc[index, founding_Field_Name]) < 1999):
                    return ("שנות התשעים")
                elif (int(table.loc[index, founding_Field_Name]) > 2000) and ( int(table.loc[index, founding_Field_Name]) < 2009):
                    return ("עשור הראשון של המאה ה-21")
                elif (int(table.loc[index, founding_Field_Name]) > 2020) and ( int(table.loc[index, founding_Field_Name]) < 2029):
                    return ("שנות ה-20 של המאה ה-21")
                else:
                    return ''

            except(Exception):
                print('invalid fid')