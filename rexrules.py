Rules = {
    "SQLREX": {
        "name": "SQL注入",
        "rex":"select|insert|delete|\\/\\*|\\*|\\.\\.\\/|\\.\\/|union|into|load_file|outfile|dump|group|substr|database|trancate|ascii|declare|concat|and|sleep|from",
        "risk_level": "high"
    },
    "XSSREX": {
        "name": "XSS",
        "rex": "( \\s|\\S)*((%73)|s)(\\s)*((%63)|c)(\\s)*((%72)|r)(\\s)*((%69)|i)(\\s)*((%70)|p)(\\s)*((%74)|t)(\\s|\\S)*",
        "risk_level": "medium"
    },
    "RCEREX": {
        "name": "RCE",
        "rex": "\\{pboot:if\\(([^}^\\$]+)\\)\\}([\\s\\S]*?)\\{\\/pboot:if\\}\n\n([\\w]+)([\\x00-\\x1F\\x7F\\/\\*\\<\\>\\%\\w\\s\\\\\\\\]+)?\\(\n\n(\\$_GET\\[)|(\\$_POST\\[)|(\\$_REQUEST\\[)|(\\$_COOKIE\\[)|(\\$_SESSION\\[)|(file_put_contents)|(file_get_contents)|(fwrite)|(phpinfo)|(base64)|(`)|(shell_exec)|(eval)|(fromCharCode)|(assert)|(system)|(exec)|(passthru)|(pcntl_exec)|(popen)|(open)|(proc_open)|(print_r)|(print)|(urldecode)|(chr)|(include)|(request)|(__FILE__)|(__DIR__)|(copy)|(call_user_)|(preg_replace)|(array_map)|(array_reverse)|(array_filter)|(getallheaders)|(get_headers)|(decode_string)|(htmlspecialchars)|(session_id)",
        "risk_level": "high"
    },

    "LFIREX": {
        "name": "文件包含攻击",
        "rex": "\\=(php|file|phar|zip|(compress\\.(bzip2|zlib))|data|http|https|ftp)((\\:\\/\\/)|(\\:))(filter|input|(\\/\\.\\.)|(\\.\\.\\/)|(\\/etc\\/passwd)|(\\/proc\\/self\\/environ)|(\\.)|([a-zA-Z\\/]\\:)|())",
        "risk_level": "high"
    },

    "SSRFREX": {
        "name": "SSRF",
        "rex": "(10(\\.([2][0-4]\\d|[2][5][0-5]|[01]?\\d?\\d)){3})|(172\\.([1][6-9]|[2]\\d|3[01])(\\.([2][0-4]\\d|[2][5][0-5]|[01]?\\d?\\d)){2})|(192\\.168(\\.([2][0-4]\\d|[2][5][0-5]|[01]?\\d?\\d)){2})|(localhost)|(127\\.0\\.0\\.1)",
        "risk_level": "high"
    },

    "XXEREX": {
        "name": "XXE",
        "rex": "(\\?(xml|XML))|(doctype|DOCTYPE)|((ENTITY|entity) [0-9a-zA-Z]* (SYSTEM|system))",
        "risk_level": "high"
    },

    "USERAGENTREX": {
        "name": "Invalid User Agent",
        "rex": "(HTTrack|harvest|audit|dirbuster|pangolin|nmap|sqln|-scan|hydra|Parser|libwww|BBBike|sqlmap|w3af|owasp|Nikto|fimap|havij|PycURL|zmeu|BabyKrokodil|netsparker|httperf|bench|wapiti)",
        "risk_level": "high"
    }
}



