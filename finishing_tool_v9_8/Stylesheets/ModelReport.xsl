<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
                xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' 
                xmlns:esri="http://schemas.esri.com/ArcGis/Server/Core/">
<xsl:output method="html"/>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                      Root Template                           -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="/">
  <html><xsl:text xml:space="preserve">&#x0D;&#x0A;</xsl:text>
<xsl:comment>&#x20;saved from url=(0016)http://localhost&#x20;</xsl:comment><xsl:text xml:space="preserve">&#x0D;&#x0A;</xsl:text>
    <head>
      <title>Model Report</title>
      <script language="JScript">
        function ExpandIt(d, i) {
          newSrc = &quot;<xsl:value-of select="ModelReport/CommonPath"/>&quot;;
<![CDATA[

          if (d.style.display == "none") {
            d.style.display = "block";
            newSrc += "/triangle2.gif";
          }
          else
          {
            d.style.display = "none";
            newSrc += "/triangle.gif";
          }
          i.src = newSrc;
        }

        // Global expanded variable
        isExpanded = false;

        function ExpandCollapseAll() {
          // Show/hide the DIV elements
          //
          divColl = document.all.tags("DIV");
          for (i=0; i<divColl.length; i++) {
            curElem = divColl(i);
            if (curElem.id.indexOf("Div") != -1) {
              curElem.style.display = (isExpanded) ? "none" : "block";
            }
          }
          // Change the source for all IMG elements
          //
]]>
          newSrc = &quot;<xsl:value-of select="ModelReport/CommonPath"/>&quot;;
<![CDATA[
          if (isExpanded)
            newSrc += "/triangle.gif";
          else
            newSrc += "/triangle2.gif";

          imgColl = document.images;
          for (i=0; i<imgColl.length; i++) {
            curElem = imgColl(i);
            if (curElem.id.indexOf("DivImg") != -1) {
              curElem.src = newSrc;
            }
          }
  
          isExpanded = !isExpanded;
        }
]]>
      </script>
    </head>
    <body>
      <table border="0" width="100%">
        <tr valign="top" bgcolor="buttonface">
          <td width="70%"><h2><u>Model Report</u></h2></td>
          <td width="30%" align="right" valign="top">
            <a href="#" onClick="ExpandCollapseAll()">Expand/Collapse All</a>
          </td>
        </tr>
      </table><br/>
      <xsl:apply-templates/>
    </body>
  </html>
</xsl:template>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                   ModelReport Template                       -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="ModelReport">
  <i>Generated on: <xsl:value-of select="GeneratedDate"/></i><br/><br/>
  <xsl:apply-templates/>
</xsl:template>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                     MdModel Template                         -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="MdModel">
  <xsl:apply-templates select="Variables"/>
  <xsl:apply-templates select="Processes"/>
</xsl:template>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                    Variables Template                        -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="Variables">
  <table border="0" width="100%">
    <tr valign="top" bgcolor="buttonface" >
    <td><h2>
      <u>Variables</u>
    </h2></td>
    </tr>
  </table><br/>

  <div style="display:block">
    <table border="0" width="100%">
      <td width="2%"></td>
      <td width="98%"> 
      <xsl:apply-templates/>
      </td>
    </table>
    <br/>
  </div>
</xsl:template>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                    MdVariable Template                       -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="MdVariable">
  <table border="0" width="100%">
    <tr valign="top" bgcolor="buttonface" style="cursor:hand;"
        onClick="ExpandIt({ReportElementId}Div, {ReportElementId}DivImg)" >
    <td><b>
      <img id="{ReportElementId}DivImg" src="{/ModelReport/CommonPath}/triangle.gif" /> 
      <xsl:value-of select="Name"/>
    </b></td>
    </tr>
  </table>
  <div id="{ReportElementId}Div" style="display:none">
    <table border="0" width="100%">
      <td width="2%"></td>
      <td width="98%">
      <b><i>Data Type:</i></b><xsl:value-of select="DataTypeDescription" /><br/>
      <b><i>Value:</i></b><xsl:value-of select="ValueAsText" /><br/>
      <xsl:apply-templates select="GPMessages"/>
      </td>
    </table>
  </div>
</xsl:template>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                    Processes Template                        -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="Processes">
  <table border="0" width="100%">
    <tr valign="top" bgcolor="buttonface" >
    <td><h2>
      <u>Processes</u>
    </h2></td>
    </tr>
  </table><br/>

  <div style="display:block">
    <table border="0" width="100%">
      <td width="2%"></td>
      <td width="98%"> 
      <xsl:apply-templates/>
      </td>
    </table>
    <br/>
  </div>
</xsl:template>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                    MdProcess Template                        -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="MdProcess">
  <table border="0" width="100%">
    <tr valign="top" bgcolor="buttonface" style="cursor:hand;"
        onClick="ExpandIt({ReportElementId}Div, {ReportElementId}DivImg)" >
    <td><b>
      <img id="{ReportElementId}DivImg" src="{/ModelReport/CommonPath}/triangle.gif" /> 
      <xsl:value-of select="Name"/>
    </b></td>
    </tr>
  </table>
  <div id="{ReportElementId}Div" style="display:none">
    <table border="0" width="100%">
      <td width="2%"></td>
      <td width="98%">
      <b><i>Tool Name:</i></b><xsl:value-of select="Tool/DisplayName"/><br/> 
      <b><i>Tool Source:</i></b><xsl:value-of select="Tool/PathName"/><br/>
      <xsl:apply-templates select="Parameters"/>
      <xsl:apply-templates select="GPMessages"/>
      </td>
    </table>
  </div>
</xsl:template>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                    Parameters Template                       -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="Parameters">
  <table border="0" width="100%">
    <tr valign="top" bgcolor="threedlightshadow" style="cursor:hand;"
        onClick="ExpandIt({./../ReportElementId}ParamDiv, {./../ReportElementId}ParamDivImg)" >
    <td>
      <img id="{./../ReportElementId}ParamDivImg" 
           src="{/ModelReport/CommonPath}/triangle.gif" /> 
      <b>Parameters:</b>
    </td>
    </tr>
  </table>
  <div id="{./../ReportElementId}ParamDiv" style="display:none">

  <!-- <table border="1" cellspacing="1" cellpadding="4" width="100%"> -->
  <table border="1" width="100%">
    <th><i>Name</i></th>
    <th><i>Direction</i></th>
    <th><i>Type</i></th>
    <th><i>Data Type</i></th>
    <th><i>Value</i></th>
    <xsl:apply-templates />
  </table>

  <br/>
  </div>
</xsl:template>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                   MdParameter Template                       -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="MdParameter">
  <tr valign="top">
    <td><b><xsl:value-of select="DisplayName"/></b></td>
    <td>
      <xsl:choose>
        <xsl:when test="ParameterDirection = 0">Input</xsl:when>
        <xsl:when test="ParameterDirection = 1">Output</xsl:when>
      </xsl:choose>
    </td>
    <td>
      <xsl:choose>
        <xsl:when test="ParameterType = 0">Required</xsl:when>
        <xsl:when test="ParameterType = 1">Optional</xsl:when>
        <xsl:when test="ParameterType = 2">Derived</xsl:when>
      </xsl:choose>
    </td>
    <td><xsl:value-of select="DataTypeDescription"/></td>
    <td><xsl:value-of select="ValueAsText"/></td>
  </tr>
</xsl:template>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                   GPMessages Template                        -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="GPMessages">
  <table border="0" width="100%">
    <tr valign="top" bgcolor="threedlightshadow" style="cursor:hand;"
        onClick="ExpandIt({./../ReportElementId}MsgDiv, {./../ReportElementId}MsgDivImg)" >
      <td>
        <img id="{./../ReportElementId}MsgDivImg" 
             src="{/ModelReport/CommonPath}/triangle.gif" /> 
        <b>Messages:</b>
      </td>
    </tr>
  </table>
  <div id="{./../ReportElementId}MsgDiv" style="display:none">

  <table border="0" cellspacing="1" cellpadding="4" width="90%">
    <xsl:apply-templates />
  </table>

  <br/>
  </div>
</xsl:template>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                    GPMessage Template                        -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="GPMessage">
  <tr valign="top">
    <td width='17'>
      <xsl:choose>
        <xsl:when test="MessageType = 2 or MessageType = 3">
          <img src="{/ModelReport/CommonPath}/msgtime.gif" /> 
        </xsl:when>
        <xsl:when test="MessageType &gt;= 0 and MessageType &lt; 50">
          <img src="{/ModelReport/CommonPath}/msginfo.gif" /> 
        </xsl:when>
        <xsl:when test="MessageType &gt;= 50 and MessageType &lt; 100">
          <img src="{/ModelReport/CommonPath}/msgwarning.gif" /> 
        </xsl:when>
        <xsl:when test="MessageType &gt;= 100">
          <img src="{/ModelReport/CommonPath}/msgerror.gif" /> 
        </xsl:when>
        <xsl:otherwise>
          <img src="{/ModelReport/CommonPath}/msgempty.gif" /> 
        </xsl:otherwise>
      </xsl:choose>
    </td>
    <td>
      <xsl:value-of select="MessageDescription"/> 
      <xsl:if test="MessageErrorCode != 0">
        (<xsl:value-of select="MessageErrorCode"/>) 
      </xsl:if>
    </td>
  </tr>
</xsl:template>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                     Generic Template                         -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="*">
</xsl:template>

</xsl:stylesheet>
