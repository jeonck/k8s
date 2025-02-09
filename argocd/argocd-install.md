# 리소스 생성   
kubectl create namespace argocd   
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/ha/install.yaml   

# 시크릿 생성   
kubectl create secret tls tls-argocd --key sample.pem --cert sample_chain_crt.pem -n argocd   

# 설치 후 패스워드 찾기    
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode; echo  
