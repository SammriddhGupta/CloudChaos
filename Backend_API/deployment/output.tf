output "api_endpoint" {
  value = data.aws_apigatewayv2_api.api_gateway_global.api_endpoint
}

output "preprocessing" {
  value = aws_apigatewayv2_route.preprocessing.route_key
}

output "preprocessing-2" {
  value = aws_apigatewayv2_route.preprocessing-2.route_key
}

output "retrieval" {
  value = aws_apigatewayv2_route.retrieval.route_key
}

output "preprocessing-final" {
  value = aws_apigatewayv2_route.preprocessing-final.route_key
}
