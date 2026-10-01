<?xml version="1.0" encoding="UTF-8"?>
<!--
  LEGACY ARTIFACT: TRACE SEPA Instant Routing & Cutoff Transform (XSLT 1.0)
  System: EuroBank TRACE Payment Gateway (Legacy Brownfield - CoreMod 2030 Scope)
  Last Modified: 2018-11-14 (Undocumented inline hotfixes)
  Target Migration: Java 21 com.fsi.payments.SepaInstantValidator (Story COREMOD-4821)
-->
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:pacs="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08">

  <xsl:output method="xml" indent="yes"/>

  <!-- EPC SCT Inst Hard SLA Cutoff: 10,000 milliseconds (inclusive) -->
  <xsl:variable name="SCT_INST_MAX_MS" select="10000"/>
  <!-- Unreachable Target2 / TIPS test routing prefix -->
  <xsl:variable name="UNREACHABLE_BIC_PREFIX" select="'XX00'"/>

  <xsl:template match="/pacs:Document/pacs:FIToFICstmrCdtTrf/pacs:CdtTrfTxInf">
    <xsl:variable name="elapsedMs" select="number(pacs:SplmtryData/pacs:Envlp/pacs:ElapsedMs)"/>
    <xsl:variable name="debtorBic" select="string(pacs:DbtrAgt/pacs:FinInstnId/pacs:BICFI)"/>
    <xsl:variable name="creditorBic" select="string(pacs:CdtrAgt/pacs:FinInstnId/pacs:BICFI)"/>

    <TraceRoutingDecision>
      <xsl:choose>
        <!-- FI-01: Reject if settlement latency exceeds 10,000 ms -->
        <xsl:when test="$elapsedMs &gt; $SCT_INST_MAX_MS">
          <Accepted>false</Accepted>
          <IsoStatusReason>AB05</IsoStatusReason>
          <LegacyRuleCode>SCT_INST_TIMEOUT_10S</LegacyRuleCode>
        </xsl:when>

        <!-- FI-04: Reject if Debtor or Creditor BIC is missing or starts with XX00 -->
        <xsl:when test="string-length($debtorBic) &lt; 8 or string-length($creditorBic) &lt; 8 or starts-with($debtorBic, $UNREACHABLE_BIC_PREFIX) or starts-with($creditorBic, $UNREACHABLE_BIC_PREFIX)">
          <Accepted>false</Accepted>
          <IsoStatusReason>RC01</IsoStatusReason>
          <LegacyRuleCode>AT_018_INVALID_BIC_ROUTING</LegacyRuleCode>
        </xsl:when>

        <xsl:otherwise>
          <Accepted>true</Accepted>
          <IsoStatusReason>ACCP</IsoStatusReason>
          <LegacyRuleCode>TRACE_ROUTING_OK</LegacyRuleCode>
        </xsl:otherwise>
      </xsl:choose>
    </TraceRoutingDecision>
  </xsl:template>
</xsl:stylesheet>
