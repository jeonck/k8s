Helm을 사용하여 Kubernetes 애플리케이션을 배포하는 과정에서 차트를 .tgz 파일로 저장하는 것은 매우 중요한 단계입니다. 이 과정은 여러 가지 이유로 핵심적입니다.

## **차트를 .tgz로 저장하는 이유**

1. **패키징 및 배포 용이성**: Helm 차트는 Kubernetes 리소스를 정의하는 템플릿의 집합입니다. 이 차트를 .tgz 파일로 패키징하면, 여러 환경에서 쉽게 배포할 수 있습니다. 패키징된 차트는 Helm 저장소에 업로드되어 다른 사용자와 공유할 수 있습니다.

2. **무결성 보장**: .tgz 파일로 패키징할 때, 차트의 무결성을 보장하기 위해 사이닝을 추가할 수 있습니다. 이는 패키지가 변조되지 않았음을 확인하는 데 도움이 됩니다. Helm은 설치 시 이 무결성을 검증하여 안전한 배포를 보장합니다.

3. **버전 관리**: .tgz 파일은 차트의 특정 버전을 명확히 정의할 수 있게 해줍니다. 이를 통해 다양한 버전의 차트를 관리하고, 필요에 따라 특정 버전을 설치할 수 있습니다.

4. **효율적인 저장소 관리**: Helm 차트는 HTTP 서버에 저장될 수 있으며, .tgz 파일은 이러한 저장소에서 쉽게 관리될 수 있습니다. Helm 저장소는 차트의 메타데이터를 포함하는 index.yaml 파일과 함께 .tgz 파일을 저장하여, 사용자들이 필요한 차트를 쉽게 검색하고 설치할 수 있도록 합니다.

## **결론**

따라서, Helm 차트를 .tgz 파일로 저장하는 것은 Kubernetes 애플리케이션의 배포 및 관리에 있어 필수적인 과정입니다. 이는 패키징, 무결성 검증, 버전 관리 및 효율적인 저장소 관리를 가능하게 하여, 전체적인 배포 프로세스를 간소화하고 안전하게 만듭니다.
[1] https://developer.harness.io/docs/self-managed-enterprise-edition/install/install-in-an-air-gapped-environment/
[2] https://docs.camunda.io/docs/self-managed/setup/guides/air-gapped-installation/
[3] https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/other-installation-methods/air-gapped-helm-cli-install/install-rancher-ha
[4] https://github.com/helm/helm/issues/12893
[5] https://docs.gitguardian.com/self-hosting/installation/airgap-installation-existing-cluster-helm
[6] https://helm.sh/docs/intro/install/
[7] https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/other-installation-methods/air-gapped-helm-cli-install
[8] https://community.sonarsource.com/t/helm-to-deploy-lts-enterprise-in-to-air-gapped-kubernetes/63076
[9] https://documentation.immuta.com/latest/configuration/self-managed-deployment/configure/immuta-in-an-air-gapped-environment
[10] https://linux.systemv.pe.kr/kubernetes/gitlab-helm-%EC%A0%80%EC%9E%A5%EC%86%8C-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0/
[11] https://bcho.tistory.com/1341
[12] https://heuristicwave.github.io/Chart
[13] https://blog.bitnami.com/2023/08/distributing-helm-charts-is-now-easier.html
[14] https://helm.sh/ko/docs/intro/install/
[15] https://blog.naver.com/hanjh1986/222903680607?viewType=pc
[16] https://velog.io/@captain-yun/Helm-%EC%84%A4%EC%B9%98-%EA%B3%BC%EC%A0%95-%EC%A0%95%EB%A6%AC
[17] https://kubevela.io/docs/platform-engineers/system-operation/enable-addon-offline/
[18] https://cloud.google.com/artifact-registry/docs/helm/store-helm-charts?hl=ko
[19] https://dev-scratch.tistory.com/180
[20] https://www.reddit.com/r/kubernetes/comments/1jjj4vp/helm_chart_image_management_for_air_gapped_k8s/
[21] https://brownbears.tistory.com/691
[22] https://helm.sh/ko/docs/topics/architecture/
[23] https://freestrokes.tistory.com/151
[24] https://tommypagy.tistory.com/610
[25] https://vcluster.com/docs/platform/install/advanced/air-gapped
[26] https://docs.replicated.com/vendor/install-with-helm
[27] https://docs.redhat.com/ko/documentation/openshift_container_platform/4.9/html/building_applications/installing-helm
[28] https://ggil.tistory.com/276
[29] https://beer1.tistory.com/45
[30] https://cloud.google.com/artifact-registry/docs/helm/manage-charts?hl=ko
[31] https://helm.sh/ko/docs/topics/chart_repository/
[32] https://docs.aws.amazon.com/ko_kr/AmazonECR/latest/userguide/push-oci-artifact.html
[33] https://cloud.ibm.com/docs/Registry?topic=Registry-registry_helm_charts&locale=ko
[34] https://www.reddit.com/r/kubernetes/comments/14nrw9t/air_gapped_on_prem_install_what_would_you_do/?tl=ko
[35] https://www.redhat.com/ko/blog/red-hat-openshift-disconnected-installations
[36] https://docs.replicated.com/vendor/helm-install-airgap
[37] https://www.ibm.com/docs/ko/api-connect/10.0.8?topic=integration-air-gapped-installation
