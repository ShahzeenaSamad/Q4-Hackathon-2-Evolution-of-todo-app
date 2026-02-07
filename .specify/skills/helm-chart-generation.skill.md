# Helm Chart Generation Skill

## Description
Reusable skill for creating and managing Helm charts for Kubernetes deployments. Includes packaging applications, managing values files, templating resources, and deploying charts to clusters.

## When to Use
- Packaging applications for deployment
- Managing environment-specific configurations
- Simplifying complex Kubernetes deployments
- Versioning application releases
- Deploying to multiple environments (dev, staging, prod)

## Capabilities

### 1. Create Helm Chart Structure
```bash
# Create new chart
helm create todo-app

# Chart structure
todo-app/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default configuration values
├── values-dev.yaml     # Development overrides
├── values-prod.yaml    # Production overrides
├── charts/             # Dependency charts
├── templates/          # Kubernetes resource templates
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   └── _helpers.tpl    # Template helpers
└── templates/tests/    # Chart tests
```

### 2. Define Chart Metadata
```yaml
# Chart.yaml
apiVersion: v2
name: todo-app
description: A Helm chart for Todo Chatbot application
type: application
version: 1.0.0
appVersion: "1.0.0"
keywords:
  - todo
  - chatbot
  - kubernetes
maintainers:
  - name: Your Name
    email: your.email@example.com
```

### 3. Configure Default Values
```yaml
# values.yaml
# Default values for todo-app

replicaCount: 3

image:
  repository: todo-app
  pullPolicy: IfNotPresent
  tag: "1.0.0"

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: true
  annotations: {}
  name: ""

podAnnotations: {}

podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000

securityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: true

service:
  type: LoadBalancer
  port: 80
  targetPort: 8000

ingress:
  enabled: false
  className: "nginx"
  annotations: {}
  hosts:
    - host: todo-app.local
      paths:
        - path: /
          pathType: Prefix
  tls: []

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}

# Environment-specific configuration
config:
  logLevel: info
  apiTimeout: 30

# Secrets (use --set-file or external secrets)
secrets:
  enabled: false
  databaseUrl: ""
  openaiApiKey: ""
```

### 4. Create Deployment Template
```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-app.fullname" . }}
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "todo-app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "todo-app.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "todo-app.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
      - name: {{ .Chart.Name }}
        securityContext:
          {{- toYaml .Values.securityContext | nindent 10 }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: {{ .Values.service.targetPort }}
          protocol: TCP
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
        env:
        - name: LOG_LEVEL
          value: {{ .Values.config.logLevel | quote }}
        - name: API_TIMEOUT
          value: {{ .Values.config.apiTimeout | quote }}
        {{- if .Values.secrets.enabled }}
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: {{ include "todo-app.fullname" . }}-secrets
              key: database-url
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: {{ include "todo-app.fullname" . }}-secrets
              key: openai-api-key
        {{- end }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

### 5. Create Service Template
```yaml
# templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "todo-app.fullname" . }}
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "todo-app.selectorLabels" . | nindent 4 }}
```

### 6. Create ConfigMap Template
```yaml
# templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "todo-app.fullname" . }}-config
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
data:
  LOG_LEVEL: {{ .Values.config.logLevel | quote }}
  API_TIMEOUT: {{ .Values.config.apiTimeout | quote }}
```

### 7. Create Secret Template
```yaml
# templates/secret.yaml
{{- if .Values.secrets.enabled }}
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "todo-app.fullname" . }}-secrets
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
type: Opaque
data:
  database-url: {{ .Values.secrets.databaseUrl | b64enc | quote }}
  openai-api-key: {{ .Values.secrets.openaiApiKey | b64enc | quote }}
{{- end }}
```

### 8. Create HPA Template
```yaml
# templates/hpa.yaml
{{- if .Values.autoscaling.enabled }}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "todo-app.fullname" . }}
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "todo-app.fullname" . }}
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
  metrics:
  {{- if .Values.autoscaling.targetCPUUtilizationPercentage }}
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: {{ .Values.autoscaling.targetCPUUtilizationPercentage }}
  {{- end }}
  {{- if .Values.autoscaling.targetMemoryUtilizationPercentage }}
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: {{ .Values.autoscaling.targetMemoryUtilizationPercentage }}
  {{- end }}
{{- end }}
```

### 9. Create Helper Templates
```yaml
# templates/_helpers.tpl
{{/*
Expand the name of the chart.
*/}}
{{- define "todo-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "todo-app.fullname" -}}
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
{{- define "todo-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-app.labels" -}}
helm.sh/chart: {{ include "todo-app.chart" . }}
{{ include "todo-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "todo-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "todo-app.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "todo-app.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
```

### 10. Environment-Specific Values

#### Development
```yaml
# values-dev.yaml
replicaCount: 1

image:
  tag: "dev"

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: false

config:
  logLevel: debug
  apiTimeout: 60
```

#### Production
```yaml
# values-prod.yaml
replicaCount: 5

image:
  tag: "1.0.0"

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

config:
  logLevel: info
  apiTimeout: 30

ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
  hosts:
    - host: todo.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: todo-app-tls
      hosts:
        - todo.example.com
```

### 11. Deploy Helm Chart

#### Install Chart
```bash
# Install with default values
helm install todo-app ./todo-app

# Install with custom values
helm install todo-app ./todo-app -f values-dev.yaml

# Install with specific values
helm install todo-app ./todo-app \
  --set replicaCount=3 \
  --set image.tag=1.0.0

# Install with secret from file
helm install todo-app ./todo-app \
  --set-file secrets.databaseUrl=./secrets/db-url.txt \
  --set-file secrets.openaiApiKey=./secrets/api-key.txt

# Install in namespace
helm install todo-app ./todo-app -n todo-app --create-namespace
```

#### Upgrade Chart
```bash
# Upgrade with new values
helm upgrade todo-app ./todo-app -f values-prod.yaml

# Upgrade with new image
helm upgrade todo-app ./todo-app \
  --set image.tag=1.1.0

# Upgrade and reuse existing values
helm upgrade todo-app ./todo-app --reuse-values
```

#### Rollback Chart
```bash
# List revisions
helm history todo-app

# Rollback to previous version
helm rollback todo-app

# Rollback to specific revision
helm rollback todo-app 2

# Rollback with specific values
helm rollback todo-app 3 -f values-prod.yaml
```

### 12. Package and Distribute Charts

#### Package Chart
```bash
# Package chart
helm package ./todo-app

# Output: todo-app-1.0.0.tgz
```

#### Create Chart Repository
```bash
# Create index file
helm repo index .

# Directory structure:
# charts/
# ├── todo-app-1.0.0.tgz
# └── index.yaml

# Serve with GitHub Pages or web server
# helm repo add my-charts https://username.github.io/helm-charts
# helm search repo my-charts/todo-app
```

#### Install from Repository
```bash
# Add repository
helm repo add my-charts https://example.com/helm-charts

# Update repository
helm repo update

# Install chart
helm install todo-app my-charts/todo-app
```

## Best Practices

### 1. Use Values Files
```yaml
# Good: Use values.yaml
{{ .Values.replicaCount }}

# Bad: Hardcode values
replicas: 3
```

### 2. Provide Sensible Defaults
```yaml
# Good: Default values work out of the box
replicaCount: 3
image:
  tag: "1.0.0"

# Bad: No defaults
replicaCount: null
image:
  tag: null
```

### 3. Use Template Helpers
```yaml
# Good: Use helper templates
name: {{ include "todo-app.fullname" . }}

# Bad: Repeat logic
name: {{ printf "%s-%s" .Release.Name .Chart.Name }}
```

### 4. Validate Values
```yaml
{{- if not .Values.image.tag }}
{{- fail "image.tag is required" }}
{{- end }}
```

### 5. Document Required Values
```yaml
# values.yaml
# Required: Configure your secrets before deploying
secrets:
  enabled: true
  databaseUrl: "REQUIRED: Set your database URL"
  openaiApiKey: "REQUIRED: Set your OpenAI API key"
```

## Chart Testing

### Lint Chart
```bash
# Lint chart
helm lint ./todo-app

# Lint with values
helm lint ./todo-app -f values-prod.yaml
```

### Dry Run Install
```bash
# Dry run install
helm install todo-app ./todo-app --dry-run --debug

# Dry run with values
helm install todo-app ./todo-app -f values-prod.yaml --dry-run
```

### Template Rendering
```bash
# Show rendered templates
helm template todo-app ./todo-app

# Show with specific values
helm template todo-app ./todo-app -f values-prod.yaml

# Output to file
helm template todo-app ./todo-app > rendered.yaml
```

## Troubleshooting

### Chart Installation Fails
```bash
# Check Helm status
helm status todo-app

# Get pod logs
kubectl logs -l app.kubernetes.io/name=todo-app

# Describe resources
kubectl describe deployment todo-app
kubectl describe pod -l app.kubernetes.io/name=todo-app
```

### Template Errors
```bash
# Dry run with debug
helm install todo-app ./todo-app --dry-run --debug

# Validate syntax
helm lint ./todo-app

# Check template rendering
helm template todo-app ./todo-app
```

### Value Overrides
```bash
# Show current values
helm get values todo-app

# Show all values (including defaults)
helm get values todo-app --all

# Reset to defaults
helm upgrade todo-app ./todo-app --reset-values
```

## Dependencies

### Chart Dependencies
```yaml
# Chart.yaml
dependencies:
  - name: postgresql
    version: 12.x.x
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
```

### Update Dependencies
```bash
# Update dependencies
helm dependency update ./todo-app

# Pull dependencies
helm dependency build ./todo-app
```

## Dependencies
- Helm 3.x CLI tool
- Kubernetes cluster access
- kubectl CLI tool (for troubleshooting)
- Application container images

## Integration with CI/CD
- Easy to integrate with GitHub Actions, GitLab CI, Jenkins
- Supports automated deployments with `helm upgrade --install`
- Version-controlled configuration with values files
- Supports multiple environments with different values files
