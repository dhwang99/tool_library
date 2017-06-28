
awk -F"\t" '{if ($5 != "null") print $0;}' extract_urls.lst > matchvr_for_eva.lst
awk -F"\t" 'BEGIN {
    types["行程"] = "starPlan";
    types["小说"] = "original";
    types["微博"] = "weibo";
} {
    type = types[$4];
	level = 1;
	if (type == "original")
		level = 0;
    print $1"\t"$2"\t"$4"\t"type"\t"level"\t"$5;
}' matchvr_for_eva.lst > vr_match.conf
