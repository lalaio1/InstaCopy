import requests
import time
import random
import argparse
import sys
from pystyle import Colors, Colorate 
import os 
import json
import re
from urllib.parse import urlparse

teia = fr'''
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

     \_______/
 `.,-'\_____/`-.,'
  /`..'\ _ /`.,'\
 /  /`.,' `.,'\  \
/__/__/     \__\__\__
\  \  \     /  /  /
 \  \,'`._,'`./  /
  \,'`./___\,'`./
 ,'`-./_____\,-'`.
     /       \ 

--> Cloning Instagram Profile <--

'''

def print_teia():
    print(Colorate.Horizontal(Colors.red_to_white, teia))

def parse_arguments():
    parser = argparse.ArgumentParser(description='InstaCopy - Instagram Clone Tool')
    parser.add_argument('-u', '--user', required=True, help='Instagram username')
    parser.add_argument('-p', '--password', required=True, help='Instagram password')
    parser.add_argument('--tor', action='store_true', help='Use Tor proxy')
    parser.add_argument('--proxy', help='Use custom proxy')
    parser.add_argument('--random-agent', action='store_true', help='Use random user agent')
    parser.add_argument('-d', '--delay', type=float, default=1, help='Delay between requests (recommended: 1-2 seconds)')
    parser.add_argument('-t', '--target', required=True, help='Instagram target username to clone')
    
    return parser.parse_args()

args = parse_arguments()
session = requests.Session()
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
]

banner = r"""
  / _ \     _  __  _   ____  _____  ____   ____  ____ _____ __  __                  
\_\(_)/_/  | ||  \| | (_ (_`|_   _|/ () \ / (__`/ () \| ()_)\ \/ /     
 _//"\\_   |_||_|\__|.__)__)  |_| /__/\__\\____)\____/|_|    |__|    by lalao1
  /   \                       
"""

def print_banner():
    print(Colorate.Horizontal(Colors.red_to_white, banner))

def setup_session(args):
    if args.tor:
        session.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
    elif args.proxy:
        session.proxies = {
            'http': args.proxy,
            'https': args.proxy
        }

    if args.random_agent:
        session.headers.update({'User-Agent': random.choice(user_agents)})
    else:
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

def obter_csrf():
    try:
        response = session.get('https://www.instagram.com/accounts/login/')
        response.raise_for_status()
        return response.cookies.get('csrftoken'), response.cookies
    except Exception as e:
        error_exit(f"Erro ao obter CSRF: {str(e)}")

def criptografar_senha(senha: str) -> str:
    timestamp = int(time.time())
    return f"#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{senha}"

def realizar_login(username: str, senha_criptografada: str, csrf_token: str, cookies):
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.instagram.com/accounts/login/',
        'x-csrftoken': csrf_token,
    }
    payload = {
        'username': username,
        'enc_password': senha_criptografada,
        'queryParams': '{}',
        'optIntoOneTap': 'false',
    }
    
    try:
        response = session.post(url_login, data=payload, headers=headers, cookies=cookies)
        response.raise_for_status()
        return response
    except Exception as e:
        error_exit(f"Erro no login: {str(e)}")

def get_user_info(username: str):
    try:
        headers = {
            'X-CSRFToken': session.cookies.get('csrftoken'),
            'X-IG-App-ID': '936619743392459', 
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f'https://www.instagram.com/{username}/'
        }
        
        response = session.get(
            f'https://www.instagram.com/api/v1/users/web_profile_info/?username={username}',
            headers=headers
        )
        
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        try:
            response = session.get(f'https://www.instagram.com/{username}/?__a=1&__d=dis')
            response.raise_for_status()
            return response.json()
        except Exception as e2:
            error_exit(f"Erro ao obter informações: {str(e)}")

def get_user_posts(user_id, max_posts=100):
    all_posts = []
    next_max_id = None
    post_count = 0
    
    while post_count < max_posts:
        try:
            if next_max_id:
                url = f'https://www.instagram.com/api/v1/feed/user/{user_id}/?max_id={next_max_id}'
            else:
                url = f'https://www.instagram.com/api/v1/feed/user/{user_id}/'
            
            headers = {
                'X-CSRFToken': session.cookies.get('csrftoken'),
                'X-IG-App-ID': '936619743392459',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': f'https://www.instagram.com/{args.target}/'
            }
            
            response = session.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if 'items' in data and isinstance(data['items'], list):
                all_posts.extend(data['items'])
                post_count += len(data['items'])
                
                if 'next_max_id' in data and data['next_max_id']:
                    next_max_id = data['next_max_id']
                else:
                    break  
            else:
                print(f"{Colors.yellow}[!] Estrutura inesperada na resposta: {data}{Colors.reset}")
                break
                
            time.sleep(args.delay)
            
        except Exception as e:
            print(f"{Colors.red}[!] Erro ao obter posts: {str(e)}{Colors.reset}")
            break
    
    return all_posts  

def error_exit(message: str):
    print(f"{Colors.red}[!] {message}{Colors.reset}")
    sys.exit(1)

def process_user_info(user_info):
    if 'data' in user_info and 'user' in user_info['data']:
        user_data = user_info['data']['user']
        user_id = user_data.get('id', 'N/A')
        bio = user_data.get('biography', 'N/A')
        followers = user_data.get('edge_followed_by', {}).get('count', 'N/A')
        following = user_data.get('edge_follow', {}).get('count', 'N/A')
        posts = user_data.get('edge_owner_to_timeline_media', {}).get('count', 'N/A')
        verified = user_data.get('is_verified', 'N/A')
        private = user_data.get('is_private', 'N/A')
        profile_pic = user_data.get('profile_pic_url_hd', 'N/A')
        full_name = user_data.get('full_name', 'N/A')
    elif 'graphql' in user_info and 'user' in user_info['graphql']:
        user_data = user_info['graphql']['user']
        user_id = user_data.get('id', 'N/A')
        bio = user_data.get('biography', 'N/A')
        followers = user_data.get('edge_followed_by', {}).get('count', 'N/A')
        following = user_data.get('edge_follow', {}).get('count', 'N/A')
        posts = user_data.get('edge_owner_to_timeline_media', {}).get('count', 'N/A')
        verified = user_data.get('is_verified', 'N/A')
        private = user_data.get('is_private', 'N/A')
        profile_pic = user_data.get('profile_pic_url_hd', 'N/A')
        full_name = user_data.get('full_name', 'N/A')
    else:
        error_exit("Estrutura de dados não reconhecida")
    
    return user_id, bio, followers, following, posts, verified, private, profile_pic, full_name

def download_media(url, filename, folder):
    try:
        response = session.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, filename)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Erro ao baixar {filename}: {str(e)}")
        return False

def download_profile_picture(profile_pic_url, target_username):
    try:
        if not profile_pic_url or profile_pic_url == 'N/A':
            return False
            
        parsed_url = urlparse(profile_pic_url)
        path = parsed_url.path
        ext = os.path.splitext(path)[1] or '.jpg'
        
        profile_dir = os.path.join(target_username, "profile")
        filename = f"{target_username}_profile_pic{ext}"
        
        return download_media(profile_pic_url, filename, profile_dir)
    except Exception as e:
        print(f"Erro ao baixar foto de perfil: {str(e)}")
        return False

def download_user_posts(target_username, user_id, full_name):
    try:
        posts_dir = os.path.join(target_username, "posts")
        os.makedirs(posts_dir, exist_ok=True)
        
        all_posts = get_user_posts(user_id)
        
        if not all_posts:
            print(f"{Colors.yellow}[!] Nenhum post encontrado para {target_username}{Colors.reset}")
            return True  
        
        print(f"{Colors.red}>{Colors.reset} Encontrados{Colors.red} {len(all_posts)} {Colors.reset}posts{Colors.reset}")
        
        for index, post in enumerate(all_posts):
            try:
                media_type = post.get('media_type', 1)
                
                caption = ""
                if 'caption' in post and post['caption'] is not None:
                    if isinstance(post['caption'], dict) and 'text' in post['caption']:
                        caption = post['caption']['text']
                    elif isinstance(post['caption'], str):
                        caption = post['caption']
                elif 'edge_media_to_caption' in post and 'edges' in post['edge_media_to_caption']:
                    edges = post['edge_media_to_caption']['edges']
                    if edges and isinstance(edges, list) and len(edges) > 0:
                        first_edge = edges[0]
                        if 'node' in first_edge and 'text' in first_edge['node']:
                            caption = first_edge['node']['text']
                
                safe_caption = re.sub(r'[\\/*?:"<>|]', "", caption[:50]) if caption else f"post_{index+1}"
                
                media_downloaded = False
                
                if media_type == 1:
                    image_url = None
                    if 'image_versions2' in post and 'candidates' in post['image_versions2']:
                        candidates = post['image_versions2']['candidates']
                        if candidates and len(candidates) > 0:
                            image_url = candidates[0]['url']
                    elif 'display_url' in post:
                        image_url = post['display_url']
                    elif 'carousel_media' in post:
                        carousel_media = post['carousel_media']
                        if carousel_media and len(carousel_media) > 0:
                            first_item = carousel_media[0]
                            if 'image_versions2' in first_item and 'candidates' in first_item['image_versions2']:
                                candidates = first_item['image_versions2']['candidates']
                                if candidates and len(candidates) > 0:
                                    image_url = candidates[0]['url']
                    
                    if image_url:
                        filename = f"{index+1:03d}_{safe_caption}.jpg"
                        if download_media(image_url, filename, posts_dir):
                            media_downloaded = True
                
                elif media_type == 2:
                    video_url = None
                    if 'video_versions' in post and len(post['video_versions']) > 0:
                        video_url = post['video_versions'][0]['url']
                    elif 'video_url' in post:
                        video_url = post['video_url']
                    
                    if video_url:
                        filename = f"{index+1:03d}_{safe_caption}.mp4"
                        if download_media(video_url, filename, posts_dir):
                            media_downloaded = True
                
                elif media_type == 8:
                    if 'carousel_media' in post:
                        for carousel_index, carousel_item in enumerate(post['carousel_media']):
                            carousel_media_type = carousel_item.get('media_type', 1)
                            carousel_media_url = None
                            
                            if carousel_media_type == 1:  # Imagem
                                if 'image_versions2' in carousel_item and 'candidates' in carousel_item['image_versions2']:
                                    candidates = carousel_item['image_versions2']['candidates']
                                    if candidates and len(candidates) > 0:
                                        carousel_media_url = candidates[0]['url']
                                elif 'display_url' in carousel_item:
                                    carousel_media_url = carousel_item['display_url']
                                
                                if carousel_media_url:
                                    filename = f"{index+1:03d}_{carousel_index+1}_{safe_caption}.jpg"
                                    if download_media(carousel_media_url, filename, posts_dir):
                                        media_downloaded = True
                            
                            elif carousel_media_type == 2:  # Vídeo
                                if 'video_versions' in carousel_item and len(carousel_item['video_versions']) > 0:
                                    carousel_media_url = carousel_item['video_versions'][0]['url']
                                elif 'video_url' in carousel_item:
                                    carousel_media_url = carousel_item['video_url']
                                
                                if carousel_media_url:
                                    filename = f"{index+1:03d}_{carousel_index+1}_{safe_caption}.mp4"
                                    if download_media(carousel_media_url, filename, posts_dir):
                                        media_downloaded = True
                
                if caption:
                    caption_filename = f"{index+1:03d}_{safe_caption}_caption.txt"
                    with open(os.path.join(posts_dir, caption_filename), 'w', encoding='utf-8') as f:
                        f.write(caption)
                
                post_metadata = {
                    'id': post.get('id'),
                    'timestamp': post.get('taken_at'),
                    'like_count': post.get('like_count'),
                    'comment_count': post.get('comment_count'),
                    'caption': caption,
                    'shortcode': post.get('code'),
                    'media_type': media_type,
                    'download_date': time.strftime("%Y-%m-%d %H:%M:%S")
                }
                
                metadata_filename = f"{index+1:03d}_{safe_caption}_metadata.json"
                with open(os.path.join(posts_dir, metadata_filename), 'w', encoding='utf-8') as f:
                    json.dump(post_metadata, f, indent=4, ensure_ascii=False)
                
                if media_downloaded: 
                    print(f"{Colors.red}> {Colors.reset}Post{Colors.red} {index+1}{Colors.reset} baixado{Colors.reset}")
                else:
                    print(f"{Colors.red}>{Colors.reset} Post {Colors.red}{index+1} {Colors.reset}processado mas nenhuma mídia baixada{Colors.reset}")
                
                time.sleep(args.delay)
                
            except Exception as e:
                print(f"{Colors.red}[!] Erro ao processar post {index+1}: {str(e)}{Colors.reset}")
                continue
        
        return True
        
    except Exception as e:
        print(f"{Colors.red}[!] Erro ao baixar posts: {str(e)}{Colors.reset}")
        return False

def save_profile_metadata(user_data, target_username):
    try:
        if 'data' in user_data and 'user' in user_data['data']:
            user_info = user_data['data']['user']
        elif 'graphql' in user_data and 'user' in user_data['graphql']:
            user_info = user_data['graphql']['user']
        else:
            return False
        
        metadata = {
            'username': user_info.get('username', 'N/A'),
            'full_name': user_info.get('full_name', 'N/A'),
            'biography': user_info.get('biography', 'N/A'),
            'external_url': user_info.get('external_url', 'N/A'),
            'followers': user_info.get('edge_followed_by', {}).get('count', 'N/A'),
            'following': user_info.get('edge_follow', {}).get('count', 'N/A'),
            'posts_count': user_info.get('edge_owner_to_timeline_media', {}).get('count', 'N/A'),
            'is_private': user_info.get('is_private', 'N/A'),
            'is_verified': user_info.get('is_verified', 'N/A'),
            'profile_pic_url': user_info.get('profile_pic_url_hd', 'N/A'),
            'user_id': user_info.get('id', 'N/A'),
            'download_date': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        os.makedirs(target_username, exist_ok=True)
        with open(f"{target_username}/profile_metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
        
        with open(f"{target_username}/bio.txt", 'w', encoding='utf-8') as f:
            f.write(metadata['biography'])
        
        return True
    except Exception as e:
        print(f"Erro ao salvar metadados: {str(e)}")
        return False

logged = fr"""
[ INFO ] --> LOGGED!                   
"""

def main():
    print_banner()
    setup_session(args)
    
    time.sleep(args.delay)
    csrf_token, cookies = obter_csrf()
    
    senha_criptografada = criptografar_senha(args.password)
    
    time.sleep(args.delay)
    response = realizar_login(args.user, senha_criptografada, csrf_token, cookies)
    
    if response.status_code == 200:
        dados = response.json()
        if dados.get('authenticated'):
            print(Colorate.Horizontal(Colors.red_to_white, logged))
            user_line = f"-> User: {args.user}"
            session_line = f"-> Session ID: {response.cookies.get('sessionid')}"
            print(Colorate.Horizontal(Colors.red_to_white, user_line))
            print(Colorate.Horizontal(Colors.red_to_white, session_line))
            
            time.sleep(args.delay)
            user_info_logado = get_user_info(args.user)
            
            if user_info_logado:
                user_id, bio, followers, following, posts, verified, private, profile_pic, full_name = process_user_info(user_info_logado)
                
                print(f"\n  --{Colors.red}> U{Colors.reset}ser {Colors.red}I{Colors.reset}nfo {Colors.red}<{Colors.reset}-- ")
                print(f"-{Colors.red}>{Colors.reset} Bio:{Colors.red} {bio}{Colors.reset}")
                print(f"-{Colors.red}>{Colors.reset} Seguidores:{Colors.red} {followers}{Colors.reset}")
                print(f"-{Colors.red}>{Colors.reset} Seguindo:{Colors.red} {following}{Colors.reset}")
                print(f"-{Colors.red}>{Colors.reset} Posts:{Colors.red} {posts}{Colors.reset}")
                print(f"-{Colors.red}>{Colors.reset} Verificado:{Colors.red} {verified}{Colors.reset}")
                print(f"-{Colors.red}>{Colors.reset} Privado:{Colors.red} {private}{Colors.reset}")
            
            time.sleep(args.delay)
            user_info_target = get_user_info(args.target)
            print_teia()
            
            if user_info_target:
                user_id_target, bio_target, followers_target, following_target, posts_target, verified_target, private_target, profile_pic_target, full_name_target = process_user_info(user_info_target)
                
                print(f"\n--{Colors.red}> {Colors.reset}Target: {Colors.red}{args.target}{Colors.reset}")
                print(f"-{Colors.red}> {Colors.reset}Nome: {Colors.red}{full_name_target}{Colors.reset}")
                print(f"-{Colors.red}>{Colors.reset} Seguidores: {Colors.red}{followers_target}{Colors.reset}")
                print(f"-{Colors.red}>{Colors.reset} Seguindo: {Colors.red}{following_target}{Colors.reset}")
                print(f"-{Colors.red}>{Colors.reset} Posts: {Colors.red}{posts_target}{Colors.reset}")
                print(f"-{Colors.red}> {Colors.reset}Verificado: {Colors.red}{verified_target}{Colors.reset}")
                print(f"-{Colors.red}>{Colors.reset} Privado: {Colors.red}{private_target}{Colors.reset}")

                os.makedirs(args.target, exist_ok=True)
                
                if save_profile_metadata(user_info_target, args.target):
                    print(f"{Colors.red}> {Colors.reset}Metadados do perfil salvos{Colors.reset}")
                 
                if download_profile_picture(profile_pic_target, args.target):
                    print(f"{Colors.red}> {Colors.reset}Foto de perfil baixada{Colors.reset}")
                
                if download_user_posts(args.target, user_id_target, full_name_target):
                    print(f"{Colors.red}>{Colors.reset} Posts baixados com sucesso{Colors.reset}")

                print(f"{Colors.red}> {Colors.reset}Clone do perfil{Colors.red} {args.target}{Colors.reset} concluído!{Colors.reset}")
                print(f"{Colors.red}> {Colors.reset}Todos os arquivos salvos na pasta: {Colors.red}{args.target}/{Colors.reset}")
            else:
                error_exit(f"[ {Colors.red}ERROR {Colors.reset}] Falha ao obter informações do usuário alvo")
        else:
            error_exit(f"[ {Colors.red}ERROR {Colors.reset}] Falha na autenticação. Verifique suas credenciais.")
    else:
        error_exit(f"Erro HTTP {response.status_code}")

if __name__ == "__main__":
    main()