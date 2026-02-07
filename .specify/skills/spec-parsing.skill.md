# Specification Parsing Skill

## Description
Reusable skill for parsing and interpreting deployment specifications, converting high-level requirements into concrete Kubernetes manifests, Helm charts, and infrastructure configurations. Critical for spec-driven deployment automation.

## When to Use
- Converting feature specifications into deployment artifacts
- Translating architectural requirements into Kubernetes resources
- Generating infrastructure from specification documents
- Validating that deployments match specifications
- Implementing spec-driven DevOps workflows

## Capabilities

### 1. Parse Application Specification
```yaml
# app-spec.yaml - High-level application specification
apiVersion: spec.k8s.io/v1alpha1
kind: ApplicationSpec
metadata:
  name: todo-chatbot
  version: "1.0.0"
  environment: production

spec:
  application:
    name: todo-chatbot
    description: "AI-powered todo management chatbot"
    type: fullstack

  components:
  - name: frontend
    type: frontend
    technology: nextjs
    version: "16.0"
    repository: github.com/user/todo-frontend
    branch: main

    runtime:
      port: 3000
      replicas: 2
      resources:
        cpu:
          request: "100m"
          limit: "200m"
        memory:
          request: "128Mi"
          limit: "256Mi"

    environment:
      - name: NEXT_PUBLIC_API_URL
        value: "https://api.todoapp.com"
      - name: NODE_ENV
        value: "production"

    healthCheck:
      path: /health
      interval: 30
      timeout: 10

  - name: backend
    type: backend
    technology: fastapi
    version: "0.100"
    repository: github.com/user/todo-backend
    branch: main

    runtime:
      port: 8000
      replicas: 3
      resources:
        cpu:
          request: "250m"
          limit: "500m"
        memory:
          request: "256Mi"
          limit: "512Mi"

    environment:
      - name: DATABASE_URL
        secret: database-url
      - name: OPENAI_API_KEY
        secret: openai-api-key

    healthCheck:
      path: /health
      interval: 30
      timeout: 10

    autoscaling:
      enabled: true
      minReplicas: 2
      maxReplicas: 10
      targetCPUUtilization: 70
      targetMemoryUtilization: 80

  dependencies:
  - name: database
    type: external
    technology: postgresql
    version: "16"
    provider: neon

  - name: redis
    type: optional
    technology: redis
    version: "7"
    provider: self-hosted

  networking:
    ingress:
      enabled: true
      className: nginx
      hosts:
        - host: app.todoapp.com
          paths:
            - path: /
              pathType: Prefix
      tls:
        - secretName: todo-app-tls
          hosts:
            - app.todoapp.com

    service:
      type: LoadBalancer
      annotations:
        service.beta.kubernetes.io/do-loadbalancer-protocol: "https"

  security:
    podSecurityContext:
      runAsNonRoot: true
      runAsUser: 1000
      fsGroup: 1000

    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop:
        - ALL
      readOnlyRootFilesystem: true
```

### 2. Convert to Kubernetes Deployment
```python
# spec_parser.py
import yaml
from typing import Dict, List, Any

class SpecParser:
    def __init__(self, spec_file: str):
        with open(spec_file, 'r') as f:
            self.spec = yaml.safe_load(f)

    def parse_deployment(self, component_name: str) -> Dict[str, Any]:
        """Parse component spec into Kubernetes Deployment"""
        component = self._get_component(component_name)

        deployment = {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {
                'name': component['name'],
                'labels': {
                    'app': component['name'],
                    'version': self.spec['metadata']['version']
                }
            },
            'spec': {
                'replicas': component['runtime']['replicas'],
                'selector': {
                    'matchLabels': {
                        'app': component['name']
                    }
                },
                'template': {
                    'metadata': {
                        'labels': {
                            'app': component['name']
                        }
                    },
                    'spec': {
                        'containers': [{
                            'name': component['name'],
                            'image': f"{component['name']}:{self.spec['metadata']['version']}",
                            'ports': [{
                                'containerPort': component['runtime']['port']
                            }],
                            'resources': {
                                'requests': {
                                    'cpu': component['runtime']['resources']['cpu']['request'],
                                    'memory': component['runtime']['resources']['memory']['request']
                                },
                                'limits': {
                                    'cpu': component['runtime']['resources']['cpu']['limit'],
                                    'memory': component['runtime']['resources']['memory']['limit']
                                }
                            },
                            'env': self._parse_env_vars(component),
                            'livenessProbe': self._parse_health_check(component['healthCheck'], 'liveness'),
                            'readinessProbe': self._parse_health_check(component['healthCheck'], 'readiness')
                        }],
                        'securityContext': self.spec['spec']['security']['podSecurityContext']
                    }
                }
            }
        }

        # Add autoscaling if enabled
        if component.get('autoscaling', {}).get('enabled'):
            deployment['spec']['autoscaling'] = self._parse_autoscaling(component['autoscaling'])

        return deployment

    def parse_service(self, component_name: str) -> Dict[str, Any]:
        """Parse component spec into Kubernetes Service"""
        component = self._get_component(component_name)
        networking = self.spec['spec']['networking']

        service = {
            'apiVersion': 'v1',
            'kind': 'Service',
            'metadata': {
                'name': f"{component['name']}-service",
                'annotations': networking['service'].get('annotations', {})
            },
            'spec': {
                'type': networking['service']['type'],
                'selector': {
                    'app': component['name']
                },
                'ports': [{
                    'protocol': 'TCP',
                    'port': 80,
                    'targetPort': component['runtime']['port']
                }]
            }
        }

        return service

    def parse_ingress(self) -> Dict[str, Any]:
        """Parse networking spec into Kubernetes Ingress"""
        networking = self.spec['spec']['networking']

        if not networking['ingress']['enabled']:
            return None

        ingress = {
            'apiVersion': 'networking.k8s.io/v1',
            'kind': 'Ingress',
            'metadata': {
                'name': f"{self.spec['metadata']['name']}-ingress",
                'annotations': networking['ingress'].get('annotations', {})
            },
            'spec': {
                'ingressClassName': networking['ingress']['className'],
                'rules': []
            }
        }

        for host_config in networking['ingress']['hosts']:
            rule = {
                'host': host_config['host'],
                'http': {
                    'paths': []
                }
            }

            for path_config in host_config['paths']:
                rule['http']['paths'].append({
                    'path': path_config['path'],
                    'pathType': path_config['pathType'],
                    'backend': {
                        'service': {
                            'name': 'frontend-service',
                            'port': {
                                'number': 80
                            }
                        }
                    }
                })

            ingress['spec']['rules'].append(rule)

        if networking['ingress'].get('tls'):
            ingress['spec']['tls'] = networking['ingress']['tls']

        return ingress

    def _get_component(self, name: str) -> Dict[str, Any]:
        """Get component by name"""
        for component in self.spec['spec']['components']:
            if component['name'] == name:
                return component
        raise ValueError(f"Component {name} not found")

    def _parse_env_vars(self, component: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse environment variables"""
        env_vars = []

        for env in component.get('environment', []):
            if 'secret' in env:
                env_vars.append({
                    'name': env['name'],
                    'valueFrom': {
                        'secretKeyRef': {
                            'name': f"{component['name']}-secrets",
                            'key': env['secret']
                        }
                    }
                })
            else:
                env_vars.append({
                    'name': env['name'],
                    'value': env['value']
                })

        return env_vars

    def _parse_health_check(self, health_check: Dict[str, Any], probe_type: str) -> Dict[str, Any]:
        """Parse health check into Kubernetes probe"""
        return {
            'httpGet': {
                'path': health_check['path'],
                'port': 'http'
            },
            'initialDelaySeconds': 5 if probe_type == 'readiness' else 30,
            'periodSeconds': health_check['interval'],
            'timeoutSeconds': health_check['timeout']
        }

    def _parse_autoscaling(self, autoscaling: Dict[str, Any]) -> Dict[str, Any]:
        """Parse autoscaling configuration"""
        return {
            'minReplicas': autoscaling['minReplicas'],
            'maxReplicas': autoscaling['maxReplicas'],
            'metrics': [
                {
                    'type': 'Resource',
                    'resource': {
                        'name': 'cpu',
                        'target': {
                            'type': 'Utilization',
                            'averageUtilization': autoscaling['targetCPUUtilization']
                        }
                    }
                }
            ]
        }

    def generate_all_manifests(self, output_dir: str):
        """Generate all Kubernetes manifests from spec"""
        import os
        import json

        os.makedirs(output_dir, exist_ok=True)

        for component in self.spec['spec']['components']:
            # Generate deployment
            deployment = self.parse_deployment(component['name'])
            with open(f"{output_dir}/{component['name']}-deployment.yaml", 'w') as f:
                yaml.dump(deployment, f)

            # Generate service
            service = self.parse_service(component['name'])
            with open(f"{output_dir}/{component['name']}-service.yaml", 'w') as f:
                yaml.dump(service, f)

        # Generate ingress
        ingress = self.parse_ingress()
        if ingress:
            with open(f"{output_dir}/ingress.yaml", 'w') as f:
                yaml.dump(ingress, f)

        print(f"✓ Generated Kubernetes manifests in {output_dir}")
```

### 3. Use Spec Parser
```bash
# Parse specification and generate manifests
python -c "
from spec_parser import SpecParser

parser = SpecParser('app-spec.yaml')
parser.generate_all_manifests('k8s/manifests')
"

# Output:
# k8s/manifests/
# ├── frontend-deployment.yaml
# ├── frontend-service.yaml
# ├── backend-deployment.yaml
# ├── backend-service.yaml
# └── ingress.yaml
```

### 4. Generate Helm Chart from Spec
```python
# helm_generator.py
class HelmGenerator:
    def __init__(self, spec_file: str):
        self.spec = SpecParser(spec_file)

    def generate_chart(self, output_dir: str):
        """Generate complete Helm chart from spec"""
        import os

        chart_dir = f"{output_dir}/helm-chart"
        os.makedirs(chart_dir, exist_ok=True)

        # Create Chart.yaml
        self._create_chart_yaml(chart_dir)

        # Create values.yaml
        self._create_values_yaml(chart_dir)

        # Create templates
        templates_dir = f"{chart_dir}/templates"
        os.makedirs(templates_dir, exist_ok=True)

        for component in self.spec.spec['spec']['components']:
            self._create_deployment_template(component, templates_dir)
            self._create_service_template(component, templates_dir)

        self._create_ingress_template(templates_dir)
        self._create_helpers_template(templates_dir)

        print(f"✓ Generated Helm chart in {chart_dir}")

    def _create_chart_yaml(self, chart_dir: str):
        """Create Chart.yaml"""
        chart_yaml = {
            'apiVersion': 'v2',
            'name': self.spec.spec['metadata']['name'],
            'description': self.spec.spec['spec']['application']['description'],
            'type': 'application',
            'version': self.spec.spec['metadata']['version'],
            'appVersion': self.spec.spec['metadata']['version']
        }

        with open(f"{chart_dir}/Chart.yaml", 'w') as f:
            yaml.dump(chart_yaml, f)

    def _create_values_yaml(self, chart_dir: str):
        """Create values.yaml"""
        # Generate from spec with defaults
        values = {
            'replicaCount': 3,
            'image': {
                'repository': self.spec.spec['metadata']['name'],
                'tag': self.spec.spec['metadata']['version'],
                'pullPolicy': 'IfNotPresent'
            },
            'service': {
                'type': 'LoadBalancer',
                'port': 80
            },
            'ingress': self.spec.spec['spec']['networking']['ingress'],
            'resources': {},
            'autoscaling': {}
        }

        with open(f"{chart_dir}/values.yaml", 'w') as f:
            yaml.dump(values, f, default_flow_style=False)

    def _create_deployment_template(self, component: Dict, templates_dir: str):
        """Create deployment template"""
        deployment = self.spec.parse_deployment(component['name'])

        # Convert to Jinja2 template
        template = self._to_jinja2_template(deployment)

        with open(f"{templates_dir}/{component['name']}-deployment.yaml", 'w') as f:
            f.write(template)

    def _to_jinja2_template(self, manifest: Dict) -> str:
        """Convert Kubernetes manifest to Jinja2 template"""
        # Implementation: Convert hardcoded values to template variables
        # This is a simplified example
        yaml_str = yaml.dump(manifest, default_flow_style=False)

        # Replace common patterns with template variables
        replacements = {
            "replicas: 3": "replicas: {{ .Values.replicaCount }}",
            "tag: '1.0.0'": "tag: {{ .Values.image.tag | default .Chart.AppVersion }}",
            # ... more replacements
        }

        for old, new in replacements.items():
            yaml_str = yaml_str.replace(old, new)

        return yaml_str
```

### 5. Validate Deployment Against Spec
```python
# spec_validator.py
class SpecValidator:
    def __init__(self, spec_file: str):
        self.spec = SpecParser(spec_file)

    def validate_deployment(self, deployment_name: str) -> Dict[str, Any]:
        """Validate actual deployment matches spec"""
        from kubernetes import client, config

        # Load Kubernetes config
        config.load_kube_config()

        apps_v1 = client.AppsV1Api()

        # Get actual deployment
        try:
            deployment = apps_v1.read_namespaced_deployment(
                name=deployment_name,
                namespace='default'
            )
        except client.exceptions.ApiException as e:
            return {
                'valid': False,
                'error': f"Deployment not found: {e}"
            }

        # Get expected deployment from spec
        expected = self.spec.parse_deployment(deployment_name)

        # Compare
        issues = []

        # Check replicas
        actual_replicas = deployment.spec.replicas
        expected_replicas = expected['spec']['replicas']
        if actual_replicas != expected_replicas:
            issues.append({
                'field': 'replicas',
                'expected': expected_replicas,
                'actual': actual_replicas
            })

        # Check resources
        actual_container = deployment.spec.template.spec.containers[0]
        expected_container = expected['spec']['template']['spec']['containers'][0]

        if actual_container.resources != expected_container['resources']:
            issues.append({
                'field': 'resources',
                'expected': expected_container['resources'],
                'actual': actual_container.resources.to_dict()
            })

        return {
            'valid': len(issues) == 0,
            'issues': issues
        }
```

### 6. Integration with CI/CD

#### GitHub Actions Workflow
```yaml
# .github/workflows/spec-to-k8s.yml
name: Spec to Kubernetes

on:
  push:
    paths:
    - 'specs/**'
    - 'app-spec.yaml'

jobs:
  generate-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pyyaml kubernetes

      - name: Parse spec and generate manifests
        run: |
          python -c "
          from spec_parser import SpecParser
          parser = SpecParser('app-spec.yaml')
          parser.generate_all_manifests('k8s/manifests')
          "

      - name: Validate manifests
        run: |
          kubectl apply --dry-run=client -f k8s/manifests/

      - name: Deploy to Kubernetes
        run: |
          kubectl apply -f k8s/manifests/

      - name: Validate deployment
        run: |
          python -c "
          from spec_validator import SpecValidator
          validator = SpecValidator('app-spec.yaml')
          result = validator.validate_deployment('frontend')
          assert result['valid'], f'Validation failed: {result}'
          "
```

## Best Practices

### 1. Version Your Specs
```yaml
metadata:
  version: "1.0.0"
  environment: production
  gitCommit: abc123
```

### 2. Use Schema Validation
```python
from jsonschema import validate

spec_schema = {
    "type": "object",
    "required": ["apiVersion", "kind", "metadata", "spec"],
    "properties": {
        "spec": {
            "type": "object",
            "required": ["application", "components"]
        }
    }
}

validate(instance=spec, schema=spec_schema)
```

### 3. Document Spec Changes
```bash
# Keep changelog
# CHANGELOG.md
## [1.1.0] - 2026-01-29
### Added
- Redis caching component
- Autoscaling for backend

### Changed
- Increased frontend replicas to 3
- Updated backend CPU limits
```

### 4. Test Before Deploying
```bash
# Dry run
kubectl apply -f k8s/manifests/ --dry-run=client

# Validate syntax
kubeval k8s/manifests/*.yaml

# Diff with cluster
kubectl diff -f k8s/manifests/
```

## Dependencies
- Python 3.11+
- PyYAML library
- Kubernetes Python client (for validation)
- kubectl CLI tool
- Specification documents (YAML/JSON)

## Integration with Other Skills
- **dockerfile-generation**: Parse component specs to generate Dockerfiles
- **helm-chart-generation**: Convert specs to Helm charts
- **k8s-deployment**: Generate deployments from parsed specs
- **spec-interpreter**: Use with spec-interpreter agent for complex specs
