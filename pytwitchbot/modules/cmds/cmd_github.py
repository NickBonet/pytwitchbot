from github import Github

from modules.cmds.cmdmodule import *


# Module that allows users to view latest commit into for a repository. ###
class CmdModuleGithub(CmdModule):
    def __init__(self, log, irc):
        super().__init__(log, irc)
        self.cmd_dict = {
            'grecent': {'function': self.get_last_commit,
                        'help': 'grecent <user> <repo> - Gets the latest commit from a specified repo.'}}
        self.mod_type = 'chan'
        self.git = Github(self.irc.conf.get_option('github', 'user'), self.irc.conf.get_option('github', 'pass'))

    # noinspection PyUnusedLocal
    def get_last_commit(self, userinfo, dest, args):
        commit = None
        if len(args) > 2 and args[1] != '' and args[2] != '':
            try:
                events = self.git.get_user(args[1]).get_repo(args[2]).get_events()
                for e in events:
                    if e.type == 'PushEvent':
                        commit = e
                        break

                lastcommit = commit.payload['commits'][0]
                commitauthor = lastcommit['author']
                commiturl = str(commit.repo.html_url) + "/commit/" + str(commit.payload['head'])
                self.irc.msg(dest,
                             '[GitHub] Repo URL: %s | Latest push: %s UTC | Commit Author: %s | Commit Message: %s' % (
                                 str(commit.repo.html_url), commit.created_at, str(commitauthor['name']),
                                 str(lastcommit['message'])))
                self.irc.msg(dest, '[GitHub] Full commit URL: %s' % commiturl)
            except Exception as err:
                self.log.info('Error while retrieving last commit: %s' % err)
                self.irc.msg(dest, 'Unable to retrieve repo\'s latest commit.')
        else:
            self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))

