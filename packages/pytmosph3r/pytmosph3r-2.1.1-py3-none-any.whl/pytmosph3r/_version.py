__version__ = release = '2.1.1'
try:
    import os
    import git
    repo = git.Repo(os.path.abspath(__file__), search_parent_directories=True)
    __version__ = release+"-"+repo.head.object.hexsha
except:
    pass
