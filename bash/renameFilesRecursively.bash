# search recursively files containing the pattern (micelle) and rename it by replacing the pattern (_micelle_) by an other pattern (_helmet_)
# pattern can use perl regular expressions
find . -iname "*micelle*" -exec rename -v _micelle_ _helmet_ '{}' \;
