.. code-block:: bash

	Usage: cli log [OPTIONS] [REVISION_RANGE] [PATHS]...
	
	  Show commit log.
	
	  REVISION_RANGE optional hash to start viewing log from. If of the form
	  <start_hash>..<end_hash> only show log for given range on the particular ref
	  that was provided
	
	  PATHS optional list of paths. If given, only show commits which affected the
	  given paths
	
	Options:
	  -r, --ref TEXT                  branch to list from. If not supplied the
	                                  default branch from config is used
	  -n, --number INTEGER            number of log entries to return
	  --since, --after TEXT           Only include commits newer than specific date,
	                                  such as '2001-01-01T00:00:00+00:00'
	  --until, --before TEXT          Only include commits older than specific date,
	                                  such as '2999-12-30T23:00:00+00:00'
	  --author TEXT                   Limit commits to a specific author (this is
	                                  the original committer). Supports specifying
	                                  multiple authors to filter by.
	  --committer TEXT                Limit commits to a specific committer (this is
	                                  the logged in user/account who performed the
	                                  commit). Supports specifying multiple
	                                  committers to filter by.
	  --query, --query-expression TEXT
	                                  Allows advanced filtering using the Common
	                                  Expression Language (CEL). An intro to CEL can
	                                  be found at https://github.com/google/cel-
	                                  spec/blob/master/doc/intro.md. Some examples
	                                  with usable variables 'commit.author' (string)
	                                  / 'commit.committer' (string) /
	                                  'commit.commitTime' (timestamp) /
	                                  'commit.hash' (string) / 'commit.message'
	                                  (string) / 'commit.properties' (map) are:
	                                  commit.author=='nessie_author'
	                                  commit.committer=='nessie_committer'
	                                  timestamp(commit.commitTime) >
	                                  timestamp('2021-06-21T10:39:17.977922Z')
	  --help                          Show this message and exit.
	
	

