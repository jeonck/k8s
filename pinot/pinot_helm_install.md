## repo  
helm repo add pinot https://raw.githubusercontent.com/apache/pinot/master/helm                                            
"pinot" has been added to your repositories  
 
## repo update  
helm repo update    
 
## label  
kubectl label namespace pinot app.kubernetes.io/managed-by=Helm                                                            
namespace/pinot labeled  
 
 
kubectl annotate namespace pinot meta.helm.sh/release-name=pinot                                                            
namespace/pinot annotated  
 
 
kubectl annotate namespace pinot meta.helm.sh/release-namespace=pinot                                                     
namespace/pinot annotated  
 
 
# helm install  
helm install pinot pinot/pinot -n pinot  
