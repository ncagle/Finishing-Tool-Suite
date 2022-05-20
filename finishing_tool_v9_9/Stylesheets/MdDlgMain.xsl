<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                version="1.0">

<xsl:output method="html"/>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--            MdElementDialogInfo Template                -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="MdElementDialogInfo">
<HTML><xsl:text xml:space="preserve">&#x0D;&#x0A;</xsl:text>
<xsl:comment>&#x20;saved from url=(0016)http://localhost&#x20;</xsl:comment><xsl:text xml:space="preserve">&#x0D;&#x0A;</xsl:text>
<HEAD>
<TITLE><xsl:value-of select='Title'/></TITLE>

<xsl:comment> ================ Scripts ================ </xsl:comment>
<xsl:text>&#10;</xsl:text>

<SCRIPT language="JavaScript"><xsl:text>&#10;</xsl:text>
<xsl:comment>

<![CDATA[
function UpdatePropertyIcon(img, msg)
{
  var imgSource;
  var description = "";
  if (msg && msg.IsError())
  {
    description = msg.Description;
    if (msg.Type == 101)]]>
      imgSource = &quot;<xsl:value-of select='CommonPath'/>/msgarrow.gif&quot;;
    else
      imgSource = &quot;<xsl:value-of select='CommonPath'/>/msgerror.gif&quot;;<![CDATA[
  }
  else if (msg && msg.IsWarning())
  {
    description = msg.Description;]]>
    imgSource = &quot;<xsl:value-of select='CommonPath'/>/msgwarning.gif&quot;;<![CDATA[
  }
  else
  {
    if (msg)
      description = msg.Description;]]>
    imgSource = &quot;<xsl:value-of select='CommonPath'/>/msgempty.gif&quot;;<![CDATA[
  }

  DialogControls.document.getElementById(img).alt = description;
  DialogControls.document.getElementById(img).src = imgSource;
}

function UpdatePropertyIcons()
{
  // Update the warning/error icon for each property]]>
  var msg;
<xsl:for-each select="Properties/PropertyGroup">
  <xsl:for-each select="Property">  
  msg = window.external.GetMessage(&quot;<xsl:value-of select="PropertyName"/>&quot;);
  UpdatePropertyIcon(&quot;<xsl:value-of select="PropertyName"/>Img&quot;, msg);
  </xsl:for-each>
</xsl:for-each><![CDATA[ 
}

//
// HELP TOPIC NOTES: 
//
// Originally we had onClick() handlers for the BODY, DIV, and (property) SPAN 
// elements that would display the corresponding help topic. When clicking on 
// the SPAN element ShowHelpTopic() was being called correctly, however, the 
// onClick() handler for the BODY/DIV element was immediately called, causing 
// the currently displayed help topic to change to the 'Intro' topic. 
//
// To correct this, I've changed the onClick() handler for the SPAN elements
// to set a global 'current-topic' variable (g_currentHelpTopic), and rely on 
// the onClick() handlers for the BODY/DIV elements to call ShowCurrentHelpTopic() 
// to actually display the current topic. ShowCurrentHelpTopic() clears the 
// g_currentHelpTopic variable before returning, and displays the 'Intro' 
// topic.
//

g_currentHelpTopic = '';

function ShowHelpTopic(topic)
{
  SetCurrentHelpTopic(topic);
  ShowCurrentHelpTopic();
}

function SetCurrentHelpTopic(topic)
{
  g_currentHelpTopic = topic;
}

function ShowCurrentHelpTopic()
{
  DialogHelp.document.getElementById("Intro").style.display = "none";
    
]]>
<xsl:for-each select="Properties/PropertyGroup"><xsl:for-each select="Property">  DialogHelp.document.getElementById(&quot;<xsl:value-of select="PropertyName"/>Topic&quot;).style.display = "none";
</xsl:for-each></xsl:for-each><![CDATA[

  if (g_currentHelpTopic == '')
    g_currentHelpTopic = 'Intro';

  DialogHelp.document.getElementById(g_currentHelpTopic).style.display = "block";

  g_currentHelpTopic = '';
}

function clicker(a,b) 
{
  if (a.style.display =='') 
  {
    a.style.display = 'none';
]]>    b.src='<xsl:value-of select="CommonPath"/>/triangle.gif'; <![CDATA[
  }
  else 
  {
    a.style.display='';
]]>    b.src='<xsl:value-of select="CommonPath"/>/triangle2.gif'; <![CDATA[
  }
}

function ShowArcGISHelp()
{
  window.external.ShowHelp();
}

]]>
</xsl:comment><xsl:text>&#10;</xsl:text>
</SCRIPT><xsl:text>&#10;</xsl:text>

<xsl:text>&#10;</xsl:text>
<SCRIPT language="JavaScript" FOR='window' EVENT='onunload'><xsl:text>&#10;</xsl:text>
<xsl:comment>
<![CDATA[
  window.external.UnRegisterControls();
]]>
</xsl:comment><xsl:text>&#10;</xsl:text>
</SCRIPT><xsl:text>&#10;</xsl:text>
<xsl:text>&#10;</xsl:text>

<SCRIPT src="{CommonPath}/help.js" language="JavaScript"></SCRIPT><xsl:text>&#10;</xsl:text>

</HEAD><xsl:text>&#10;</xsl:text>
<xsl:text>&#10;</xsl:text>

<xsl:comment> ================ Frames ================ </xsl:comment>
<xsl:text>&#10;</xsl:text>

<FRAMESET NAME="DialogMain" cols="*,1" FRAMEBORDER="0" FRAMESPACING="0">
  <FRAME SRC="MdDlgContent.htm" NAME="DialogControls" ID="DialogControls" FRAMEBORDER="0" SCROLLING="Auto" MARGINWIDTH="0" MARGINHEIGHT="0"></FRAME>
  <FRAME SRC='MdDlgHelp.htm' NAME='DialogHelp' ID='DialogHelp' FRAMEBORDER='1' SCROLLING='Auto' MARGINWIDTH='0' MARGINHEIGHT='0'></FRAME>
</FRAMESET>

</HTML>
</xsl:template>

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<!--                   Root Template                        -->
<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
<xsl:template match="/">
  <xsl:apply-templates />
</xsl:template>

</xsl:stylesheet>
