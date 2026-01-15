{{/*
Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
Licensed under the Apache License, Version 2.0
*/}}

{{/*
Expand the name of the chart.
*/}}
{{- define "zqautonxg.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "zqautonxg.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "zqautonxg.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "zqautonxg.labels" -}}
helm.sh/chart: {{ include "zqautonxg.chart" . }}
{{ include "zqautonxg.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: zqautonxg
{{- end }}

{{/*
Selector labels
*/}}
{{- define "zqautonxg.selectorLabels" -}}
app.kubernetes.io/name: {{ include "zqautonxg.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "zqautonxg.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "zqautonxg.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
PostgreSQL host
*/}}
{{- define "zqautonxg.postgresql.host" -}}
{{- printf "%s-postgres" (include "zqautonxg.fullname" .) }}
{{- end }}

{{/*
Redis host
*/}}
{{- define "zqautonxg.redis.host" -}}
{{- printf "%s-redis" (include "zqautonxg.fullname" .) }}
{{- end }}
