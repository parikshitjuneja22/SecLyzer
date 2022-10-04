#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Git scanning."""
from pathlib import Path
from urllib.parse import urlparse

import git

from flask import jsonify
from seclyzer import seclyzer

from web.email import email_alert

from seclyzer import (
    settings,
    utils,
)

from web.db_operations import (
    is_scan_exists,
    save_results,
)
import requests 


def lsremote(url):
    """Git ls-remote."""
    remote_refs = {}
    g = git.cmd.Git()
    for ref in g.ls_remote(url).split('\n'):
        hash_ref_list = ref.split('\t')
        remote_refs[hash_ref_list[1]] = hash_ref_list[0]
    return remote_refs

def clone(request):
    """Git clone."""
    url = request.form['url']
    score = {}
    # check if npm or git
    if url.split('/')[2] == "www.npmjs.com":    
        owner_repo = url.split('/')[4]
        req = requests.get(f"https://libraries.io/api/NPM/{owner_repo}?api_key=71e406ad31d370d18dd07f1b9d83ea93")
        npm_data = req.json()
        url = npm_data['repository_url']
        url = url + ".git"
        owner_name = url.split('/')[3]
        print(owner_name + "/" + owner_repo)
        score["rank_npm"] = npm_data['rank']
        
    elif url.split('/')[2] == "pypi.org":
        owner_repo = url.split('/')[4]
        req = requests.get(f"https://libraries.io/api/PYPI/{owner_repo}?api_key=71e406ad31d370d18dd07f1b9d83ea93")
        pypi_data = req.json()
        url = pypi_data['repository_url']
        url = url + ".git"
        owner_name = url.split('/')[3]
        print(owner_name + "/" + owner_repo)
        score["rank_pypi"] = pypi_data['rank']

    else:
        owner_name = url.split('/')[3]
        owner_repo = url.split('/')[4]
        owner_repo = owner_repo.split('.')[0]
    
    r1 = requests.get(f"https://api.github.com/repos/{owner_name}/{owner_repo}")
    data = r1.json()
    
    req_rank = requests.get(f"https://libraries.io/api/github/{owner_name}/{owner_repo}?api_key=71e406ad31d370d18dd07f1b9d83ea93")
    git_rank = req_rank.json()
    if len(git_rank) != 1:
        score["rank_git"] = git_rank['rank']
    else:
        score["rank_git"] = 0

    #pagination for checking all user repos
    results = []
    params = {'per_page':100}
    another_page = True
    api = f"https://api.github.com/users/{owner_name}/repos"
    while another_page:
        r2 = requests.get(api, params=params)
        data2 = r2.json()
        results.append(data2)
        if 'next' in r2.links:
            api = r2.links['next']['url']
        else:
            another_page = False
    # r2 = requests.get(f"https://api.github.com/users/{owner_name}/repos")
    # data_all = r2.json()
    json_name = {} # stats of all repos of the user
    for i in results:
        for j in i:
            json_name[j["name"]] = {"forks":j["forks"], "watchers":j["watchers"], "open_issues":j["open_issues"], "size":j["size"]}
    # for repo in data_all:
    #     json_name[repo['name']] = {'forks':repo['forks'], 'watchers':repo['watchers'], 'open_issues':repo['open_issues']}

    # search for duplication
    duplication = {}
    r3 = requests.get(f"https://api.github.com/search/repositories?q={owner_repo}")
    data3 = r3.json()

    for i, repo in enumerate(data3['items']):
        if repo['name'] == owner_repo:
            duplication[str(i)] = {"name":repo['name'],"full_name":repo['full_name'], "forks":repo['forks'], "watchers":repo['watchers'], "open_issues":repo['open_issues'], "html_url":repo['html_url']}

    try:
        refs = lsremote(url)
    except Exception as exp:
        return jsonify({
            'status': 'failed',
            'message': str(exp)})
    sha2 = utils.gen_sha256_hash(refs['HEAD'])
    app_dir = Path(settings.UPLOAD_FOLDER) / sha2
    if is_scan_exists(sha2):
        return jsonify({
            'status': 'success',
            'url': 'scan/' + sha2})
    if not app_dir.exists():
        print('Cloning Repository')
        git.Repo.clone_from(url, app_dir.as_posix())
    results = seclyzer.scan(app_dir.as_posix())
    results['forks'] = data['forks']
    results['watchers'] = data['watchers']
    results['open_issues'] = data['open_issues']
    results['json_name'] = json_name
    results['duplication'] = duplication
    results['score'] = score

    # Save Result
    print('Saving Scan Results!')
    filename = Path(urlparse(url).path).name
    save_results(filename, sha2, app_dir.as_posix(), results)
    email_alert(filename, sha2, request.url_root, results)
    return jsonify({
        'status': 'success',
        'url': 'scan/' + sha2})
