Kubernetes 설치 절차서 (containerd 활용)
1. Swap 비활성화
Kubernetes를 설치하기 전에 swap 메모리를 비활성화해야 합니다. 이를 통해 시스템이 swap을 사용하지 않도록 설정합니다.

# Swap 비활성화
sudo swapoff -a

# 부팅 시 swap이 다시 활성화되지 않도록 설정
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
2. 네트워크 모듈 및 sysctl 설정
K8s 설치에 필요한 네트워크 모듈을 로드하고, 필요한 sysctl 파라미터를 설정합니다.

# 네트워크 모듈 로드
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# sysctl 파라미터 설정
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

# sysctl 파라미터 적용
sudo sysctl --system
3. Containerd 설치 및 설정
Kubernetes에서는 컨테이너 런타임으로 containerd를 사용합니다. containerd를 설치하고, systemd cgroup을 설정합니다.

# containerd 설치
sudo apt install -y containerd

# containerd 설정 파일 생성 및 수정
sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml
sudo vi /etc/containerd/config.toml

# SystemdCgroup = true 로 수정 후 저장
설정이 완료된 후 containerd 서비스를 재시작하고, 상태를 확인합니다.

# containerd 서비스 재시작
sudo systemctl restart containerd.service

# 서비스 상태 확인
sudo systemctl status containerd.service
4. Kubernetes 설치
다음으로, Kubernetes를 설치합니다. 공식 저장소의 패키지를 사용하여 kubeadm, kubelet, kubectl을 설치합니다.

# K8s 설치를 위한 패키지 설정
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl

sudo mkdir -p /etc/apt/keyrings

sudo rm /etc/apt/sources.list.d/kubernetes.list

# K8s 패키지 저장소 추가
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | sudo gpg --dearmor -o /usr/share/keyrings/kubernetes-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list

# 패키지 업데이트
sudo apt-get update

# 설치 가능한 버전 확인
sudo apt-cache madison kubeadm

# kubeadm, kubelet, kubectl 설치
sudo apt-get install -y kubelet=1.29.14-1.1 kubeadm=1.29.14-1.1 kubectl=1.29.14-1.1
5. Kubernetes 클러스터 초기화
클러스터를 초기화하여 마스터 노드를 설정합니다. --apiserver-advertise-address 옵션에 마스터 노드의 IP 주소를 입력하고, --pod-network-cidr로 네트워크 CIDR을 지정합니다. (내부 IP: 192.168.0.11 / 외부 IP: 10.0.1.4 일 때)

sudo kubeadm init \ --control-plane-endpoint=10.0.1.4:6443 \ --apiserver-advertise-address=192.168.0.11 \ --pod-network-cidr=192.168.0.0/16 \ --apiserver-cert-extra-sans=10.0.1.4


sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --cri-socket=unix:///run/containerd/containerd.sock --control-plane-endpoint=10.0.1.4 --upload-certs







ㅇ 설치 중 실패 시 reset 필요 
   sudo kubeadm reset
   
   sudo rm -rf /etc/kubernetes/*
   sudo rm -rf /var/lib/etcd/*
   sudo systemctl restart kubelet




초기화가 완료되면, 클라이언트에서 K8s를 관리할 수 있도록 kubeconfig 파일을 설정합니다.

# kubeconfig 설정
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
6. k9s 설치
mkdir ~/k9s-install && cd ~/k9s-install
wget https://github.com/derailed/k9s/releases/download/v0.40.5/k9s_Linux_amd64.tar.gz
tar -zxvf k9s_Linux_amd64.tar.gz
sudo mv k9s /usr/local/bin
sudo chmod +x /usr/local/bin/k9s


7. 네트워크 플러그인 설치
Pod 간 통신을 위해 Calico 네트워크 플러그인을 설치합니다.

kubectl apply -f https://docs.projectcalico.org/v3.14/manifests/calico.yaml

kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.0/manifests/calico.yaml

7. 워커 노드에서 조인하기 
예시 

sudo kubeadm join 10.0.1.4:6443 --token wvdmu5.l50k489eaonmdm9s --discovery-token-ca-cert-hash sha256:b05497c2498cc2221d70a6e4886ea6114610d4e8e8c72044eac5fa7d61537c94 --control-plane --certificate-key b05497c2498cc2221d70a6e4886ea6114610d4e8e8c72044eac5fa7d61537c94


조인 명령어 찾기 

ㅇ 해시값 찾기 

openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'
b05497c2498cc2221d70a6e4886ea6114610d4e8e8c72044eac5fa7d61537c94
 ㅇ 조인 명령어: 위 해시값을 아래의 명령어에 활용하여 조인 명령어 도출 가능

kubeadm token create --certificate-key="b05497c2498cc2221d70a6e4886ea6114610d4e8e8c72044eac5fa7d61537c94" --print-join-command
kubeadm join 10.0.1.4:6443 --token wvdmu5.l50k489eaonmdm9s --discovery-token-ca-cert-hash sha256:b05497c2498cc2221d70a6e4886ea6114610d4e8e8c72044eac5fa7d61537c94 --control-plane --certificate-key b05497c2498cc2221d70a6e4886ea6114610d4e8e8c72044eac5fa7d61537c94


ㅇ 해시값 만료시 재생성 

# Control Plane 노드에서 새 토큰 생성
kubeadm token create --print-join-command

8. 클러스터 상태 확인
클러스터가 정상적으로 설치되었는지 확인하려면, 아래 명령어를 실행합니다.

kubectl get nodes
만약 master node를 추후에 worker node로 사용한다면 다음 명령어를 사용합니다.

kubectl taint nodes <master-node-name> node-role.kubernetes.io/control-plane-
그리고 사용하지 않는 명령어는 다음과 같습니다.

kubectl taint nodes <master-node-name> node-role.kubernetes.io/control-plane:NoSchedule
