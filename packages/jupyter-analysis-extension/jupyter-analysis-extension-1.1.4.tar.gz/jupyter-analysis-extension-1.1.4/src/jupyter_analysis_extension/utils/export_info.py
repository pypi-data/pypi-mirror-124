from xhtml2pdf import pisa

HTML_TEMPLATE = """
<html>
  <head>

    <title>{title}</title>

    <!-- Load RequireJS, used by the IPywidgets for dependency management -->
    <script 
      src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js" 
      integrity="sha256-Ae2Vz/4ePdIu6ZyI/5ZGsYnb+m0JlOmKPjt6XZ9JJkA=" 
      crossorigin="anonymous">
    </script>

    <!-- Load IPywidgets bundle for embedding. -->
    <script
      data-jupyter-widgets-cdn="https://unpkg.com/"
      data-jupyter-widgets-cdn-only
      src="https://cdn.jsdelivr.net/npm/@jupyter-widgets/html-manager@*/dist/embed-amd.js" 
      crossorigin="anonymous">
    </script>

    <!-- The state of all the widget models on the page -->
    <script type="application/vnd.jupyter.widget-state+json">
      {manager_state}
    </script>
  </head>

  <body>

    <h1 align="center">{title}</h1>

    {widget_views}

  </body>
</html>
"""

WIDGET_VIEW_TEMPLATE = """
    <h2>{title}</h2>
    <div id="{num}-slider-widget">
      <!-- This script tag will be replaced by the view's DOM tree -->
      <script type="application/vnd.jupyter.widget-view+json">
        {widget_view}
      </script>
    </div>

    <hrule />
"""


def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to receive result

    # close output file
    result_file.close()                 # close output file

    # return True on success and False on errors
    return pisa_status.err
