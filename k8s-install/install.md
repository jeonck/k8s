# Kubernetes 설치 절차서 (containerd 활용)

## **1. Swap 비활성화**

```jsx
*# Swap 비활성화*
sudo swapoff -a

*# 부팅 시 swap 비활성화 유지*
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
```

## **2. 네트워크 설정**

```jsx
*# 네트워크 모듈 로드*
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

*# sysctl 파라미터 설정*
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sudo sysctl --system
```

## **3. Containerd 설치 및 설정**

```jsx
*# containerd 설치*
sudo apt install -y containerd

*# 설정 파일 생성*
sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml

*# SystemdCgroup = true 설정*
sudo vi /etc/containerd/config.toml

*# 서비스 재시작*
sudo systemctl restart containerd.service
sudo systemctl status containerd.service
```

## **4. Kubernetes 설치**

```jsx
*# 기본 패키지 설치*
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl

*# 저장소 설정*
sudo mkdir -p /etc/apt/keyrings
sudo rm /etc/apt/sources.list.d/kubernetes.list

*# K8s 저장소 추가*
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | sudo gpg --dearmor -o /usr/share/keyrings/kubernetes-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list

*# K8s 컴포넌트 설치*
sudo apt-get update
sudo apt-get install -y kubelet=1.29.14-1.1 kubeadm=1.29.14-1.1 kubectl=1.29.14-1.1
```

## **5. 클러스터 초기화**

```jsx
*# 클러스터 초기화*
sudo kubeadm init --pod-network-cidr=10.244.0.0/16 \
  --cri-socket=unix:///run/containerd/containerd.sock \
  --control-plane-endpoint=10.0.1.4 \
  --upload-certs

*# kubeconfig 설정*
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

## **6. k9s 설치**

```jsx
mkdir ~/k9s-install && cd ~/k9s-install
wget https://github.com/derailed/k9s/releases/download/v0.40.5/k9s_Linux_amd64.tar.gz
tar -zxvf k9s_Linux_amd64.tar.gz
sudo mv k9s /usr/local/bin
sudo chmod +x /usr/local/bin/k9s
```

## **7. 네트워크 플러그인 설치**

```jsx
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.0/manifests/calico.yaml
```

## **8. 워커 노드 조인**

## **토큰 및 해시 확인**

```jsx
*# 해시값 확인*
openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'

*# 조인 명령어 생성*
kubeadm token create --print-join-command
```

## **클러스터 상태 확인**

```jsx
kubectl get nodes

*# 마스터 노드를 워커로 사용시*
kubectl taint nodes <master-node-name> node-role.kubernetes.io/control-plane-
```

## **문제 해결**

```jsx
*# 설치 실패시 초기화*
sudo kubeadm reset
sudo rm -rf /etc/kubernetes/*
sudo rm -rf /var/lib/etcd/*
sudo systemctl restart kubelet
```
