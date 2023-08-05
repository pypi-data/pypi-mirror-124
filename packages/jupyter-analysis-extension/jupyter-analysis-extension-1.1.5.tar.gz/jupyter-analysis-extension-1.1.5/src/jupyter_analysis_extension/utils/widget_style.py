import ipywidgets
from IPython.display import display, Javascript


class WidgetStyle:
    @staticmethod
    def style_default():
        style_data = ""
        style_data += WidgetStyle.style_notebook_windows()
        style_data += WidgetStyle.style_op_popup_menu()
        style_data += WidgetStyle.style_table()
        style_data += WidgetStyle.style_hyper()
        style_data += WidgetStyle.style_file_loading()
        style_data += WidgetStyle.style_check_box()

        integrated_style = ipywidgets.HTML(
            value="""
                <style>
                {0}
                </style
            """.format(style_data)
        )
        display(integrated_style)

    @staticmethod
    def style_notebook_windows():
        style_data = """
                            div#notebook-container    { width: 100%;}
                            div#menubar-container     { width: 65%; }
                            div#maintoolbar-container { width: 99%; }
                            div#output_scroll {height: 100%; }
        """
        disable_js = """
        IPython.OutputArea.prototype._should_scroll = function(lines) {
            return false;
        }
        """
        display(Javascript(disable_js))
        return style_data

    @staticmethod
    def style_op_popup_menu():
        style_data = """
                   .icon_menu {
                     overflow: visible !important;
                   }
                   .drop-img {
                     background-color: white;
                     color: white;
                     cursor: pointer;
                     border: none;
                     width: 100%; 
                     height: 100%;
                     padding : 15px;
                     position : relative;
                     top : -5px;
                   }
                   .icon-op-name {
                     position: relative;
                     text-align: center;
                     top: -24px;
                     font-size : 11px;
                     cursor: pointer;
                   }
                   .dropdown-btn {
                     width: 65px;
                     height:65px;
                     border : 1px solid grey;
                     border-radius: 14%;
                     overflow : hidden !important;
                   }
                   .dropdown {
                     width: 50px;
                     position: relative;
                     display: inline-block;
                     overflow: visible !important;
                   }
                   .dropdown-content {
                     display: none;
                     position: absolute;
                     background-color: white;
                     min-width: 200px;
                     box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
                     z-index: 100;
                     cursor: pointer;
                   }
                   .dropdown-content a {
                     color: black;
                     padding: 10px;
                     text-decoration: none;
                     display: block;
                     min-width: 200px;
                     cursor: pointer;
                   }
                   .dropdown:hover .drop-img {
                     background-color: aliceblue;
                   }
                   .dropdown-content a:hover {
                     background-color: aliceblue;
                   }
                   .dropdown:hover .dropdown-content {
                     display: block;
                   }
                """
        return style_data

    @staticmethod
    def style_table():
        style_data = """
                    .styledTable {
                      border-collapse: collapse;
                      text-align: left;
                      line-height: 1.5;
                    }
                    .styledTable thead th {
                      padding: 10px;
                      font-weight: bold;
                      vertical-align: top;
                      color: #369;
                      border-bottom: 3px solid #036;
                    }
                    .styledTable tbody th {
                      width: 150px;
                      padding: 10px;
                      font-weight: bold;
                      vertical-align: top;
                      border-bottom: 1px solid #ccc;
                      background: #f3f6f7;
                    }
                    .styledTable td {
                      width: 350px;
                      padding: 10px;
                      vertical-align: top;
                      border-bottom: 1px solid #ccc;
                    }
                """
        return style_data

    @staticmethod
    def style_hyper():
        style_data ="""
                    .round-button-5 {
                      border-radius: 5px;
                    }
                    .multiple-select-title {
                      border : 1px solid gray;
                      border-bottom : 0px;
                      padding: 0px 10px;
                      background-color : #eeeeee;
                    }
                """
        return style_data

    @staticmethod
    def style_file_loading():
        style_data ="""
                     @keyframes rotate {
                        from {
                            transform: rotate(0deg);
                        }
                        to { 
                            transform: rotate(360deg);
                        }
                    }
                     @-webkit-keyframes rotate {
                        from {
                            -webkit-transform: rotate(0deg);
                        }
                        to { 
                            -webkit-transform: rotate(360deg);
                        }
                    }
                    .load {
                        width: 23px;
                        height: 23px;
                        margin: 10px auto 0;
                        margin-left : 10px;
                        border:solid 5px #8822aa;
                        border-radius: 50%;
                        border-right-color: transparent;
                        border-bottom-color: transparent;
                         -webkit-transition: all 0.5s ease-in;
                        -webkit-animation-name:             rotate; 
                        -webkit-animation-duration:         1.0s; 
                        -webkit-animation-iteration-count:  infinite;
                        -webkit-animation-timing-function: linear;
                             transition: all 0.5s ease-in;
                        animation-name:             rotate; 
                        animation-duration:         1.0s; 
                        animation-iteration-count:  infinite;
                        animation-timing-function: linear; 
                    }
                """
        return style_data

    @staticmethod
    def style_check_box():
        style_data ="""
                    .styled-check-box {
                        height : 20px;
                        overflow : hidden !important;
                    }
                """
        return style_data